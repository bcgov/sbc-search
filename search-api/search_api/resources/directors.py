# Copyright © 2020 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from tempfile import NamedTemporaryFile

from flask import Blueprint, request, jsonify, send_from_directory
from openpyxl import Workbook

from search_api.auth import jwt
from search_api.models import (
    Corporation,
    CorpOpState,
    CorpState,
    CorpParty,
    CorpName,
    Address,
    Office,
    OfficeType,
    OfficesHeld,
    OfficerType,
    Event,
    Filing,
    FilingType,
    _get_corpparty_search_results,
    _merge_corpparty_search_addr_fields,
    _normalize_addr,
)
from search_api.constants import STATE_TYP_CD_ACT, STATE_TYP_CD_HIS

API = Blueprint('DIRECTORS_API', __name__, url_prefix='/api/v1/directors')


@API.route('/')
@jwt.requires_auth
def hello():
    return "Welcome to the director search API."


@API.route('/search/')
@jwt.requires_auth
# @jwt.requires_auth
def corpparty_search():
    args = request.args
    results = _get_corpparty_search_results(args)

    # Total number of results
    # This is waaay to expensive on a large db.
    # total_results = results.count()

    # Pagination
    page = int(args.get("page")) if "page" in args else 1
    results = results.paginate(int(page), 20, False)

    corp_parties = []
    for row in results.items:
        result_fields = [
            'corp_party_id', 'first_nme', 'middle_nme', 'last_nme', 'appointment_dt', 'cessation_dt',
            'corp_num', 'corp_nme', 'party_typ_cd', 'state_typ_cd', 'postal_cd']
        result_dict = {key: getattr(row, key) for key in result_fields}
        result_dict['corp_party_id'] = int(result_dict['corp_party_id'])
        result_dict['addr'] = _merge_corpparty_search_addr_fields(row)

        corp_parties.append(result_dict)

    return jsonify({'results': corp_parties})


@API.route('/search/export/')
@jwt.requires_auth
def corpparty_search_export():

    # Query string arguments
    args = request.args

    # Fetching results
    results = _get_corpparty_search_results(args)

    # Exporting to Excel
    wb = Workbook()

    export_dir = "/tmp"
    with NamedTemporaryFile(mode='w+b', dir=export_dir, delete=True):

        sheet = wb.active

        # Sheet headers (first row)
        _ = sheet.cell(column=1, row=1, value="Filing #")
        _ = sheet.cell(column=2, row=1, value="Surname")
        _ = sheet.cell(column=3, row=1, value="First Name")
        _ = sheet.cell(column=4, row=1, value="Middle Name")
        _ = sheet.cell(column=5, row=1, value="Address")
        _ = sheet.cell(column=6, row=1, value="Postal Code")
        _ = sheet.cell(column=7, row=1, value="Office Held")
        _ = sheet.cell(column=8, row=1, value="Appointed")
        _ = sheet.cell(column=9, row=1, value="Ceased")
        _ = sheet.cell(column=10, row=1, value="Company Status")
        _ = sheet.cell(column=11, row=1, value="Company Name")
        _ = sheet.cell(column=12, row=1, value="Inc/Reg #")

        for index, row in enumerate(results, 2):
            # CorpParty.corp_party_id
            _ = sheet.cell(column=1, row=index, value=row.corp_party_id)
            # CorpParty.last_nme
            _ = sheet.cell(column=2, row=index, value=row.last_nme)
            # CorpParty.first_nme
            _ = sheet.cell(column=3, row=index, value=row.first_nme)
            # CorpParty.middle_nme
            _ = sheet.cell(column=4, row=index, value=row.middle_nme)
            # Address.addr_line_1, Address.addr_line_2, Address.addr_line_3
            _ = sheet.cell(column=5, row=index, value=_merge_corpparty_search_addr_fields(row))
            # Address.postal_cd
            _ = sheet.cell(column=6, row=index, value=row.postal_cd)
            # CorpParty.party_typ_cd
            _ = sheet.cell(column=7, row=index, value=row.party_typ_cd)
            # CorpParty.appointment_dt
            _ = sheet.cell(column=8, row=index, value=row.appointment_dt)
            # CorpParty.cessation_dt
            _ = sheet.cell(column=9, row=index, value=row.cessation_dt)
            # CorpOpState.state_typ_cd
            _ = sheet.cell(column=10, row=index, value=_get_state_typ_cd_display_value(row.state_typ_cd))
            # CorpName.corp_nme
            _ = sheet.cell(column=11, row=index, value=row.corp_nme)
            # Corporation.corp_num
            _ = sheet.cell(column=12, row=index, value=row.corp_num)

        current_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
        filename = "Director Search Results {date}.xlsx".format(date=current_date)
        full_filename_path = "{dir}/{filename}".format(dir=export_dir, filename=filename)
        wb.save(filename=full_filename_path)

        return send_from_directory(export_dir, filename, as_attachment=True)


@API.route('/<id>')
@jwt.requires_auth
def person(id):
    result = (
        CorpParty.query
        .join(Corporation, Corporation.corp_num == CorpParty.corp_num)
        .add_columns(
            Corporation.corp_typ_cd,
            Corporation.admin_email
        ).filter(CorpParty.corp_party_id == int(id))).one()

    person = result[0]
    result_dict = {}

    filing_description = (
        CorpParty.query
        .join(Event, Event.event_id == CorpParty.start_event_id)
        .join(Filing, Filing.event_id == Event.event_id)
        .join(FilingType, FilingType.filing_typ_cd == Filing.filing_typ_cd)
        .add_columns(FilingType.full_desc)
        .filter(CorpParty.corp_party_id == int(id)).all())

    name = CorpName.query.filter(CorpName.corp_num == person.corp_num).add_columns(
        CorpName.corp_nme).filter()[0]  # TODO: handle multiple names
    offices = Office.query.filter(Office.corp_num == person.corp_num).all()
    delivery_addr = _normalize_addr(person.delivery_addr_id)
    mailing_addr = _normalize_addr(person.mailing_addr_id)

    states = CorpState.query.filter(
        CorpState.corp_num == person.corp_num,
        CorpState.end_event_id == None).all()  # noqa

    # TODO : list all, or just the one from the correct time.
    corp_delivery_addr = _normalize_addr(offices[0].delivery_addr_id) if offices else ''
    corp_mailing_addr = _normalize_addr(offices[0].mailing_addr_id) if offices else ''

    # TODO: switch to marshmallow.
    result_dict['corp_party_id'] = int(person.corp_party_id)
    result_dict['first_nme'] = person.first_nme
    result_dict['middle_nme'] = person.middle_nme
    result_dict['last_nme'] = person.last_nme
    result_dict['appointment_dt'] = person.appointment_dt
    result_dict['cessation_dt'] = person.cessation_dt
    result_dict['corp_num'] = person.corp_num
    result_dict['corp_nme'] = name.corp_nme
    result_dict['party_typ_cd'] = person.party_typ_cd
    result_dict['corp_party_email'] = person.email_address
    result_dict['delivery_addr'] = delivery_addr
    result_dict['mailing_addr'] = mailing_addr
    result_dict['corp_delivery_addr'] = corp_delivery_addr
    result_dict['corp_mailing_addr'] = corp_mailing_addr
    result_dict['corp_typ_cd'] = result[1]
    result_dict['corp_admin_email'] = result[2]
    result_dict['full_desc'] = filing_description[0].full_desc if filing_description else None

    result_dict['states'] = [s.as_dict() for s in states]

    return jsonify(result_dict)


@API.route('/officesheld/<corppartyid>')
@jwt.requires_auth
def officesheld(corppartyid):
    results = (
        OfficerType.query
        .join(OfficesHeld, OfficerType.officer_typ_cd == OfficesHeld.officer_typ_cd)
        .join(CorpParty, OfficesHeld.corp_party_id == CorpParty.corp_party_id)
        # .join(Address, CorpParty.mailing_addr_id == Address.addr_id)
        .join(Event, Event.event_id == CorpParty.start_event_id)
        .add_columns(
            CorpParty.corp_party_id,
            OfficerType.officer_typ_cd,
            OfficerType.short_desc,
            CorpParty.appointment_dt,
            Event.event_timestmp
        )
        .filter(CorpParty.corp_party_id == int(corppartyid))
    )

    offices = []
    for row in results:
        result_dict = {}

        result_dict['corp_party_id'] = int(row[1])
        result_dict['officer_typ_cd'] = row[2]
        result_dict['short_desc'] = row[3]
        result_dict['appointment_dt'] = row[4]
        result_dict['year'] = row[5].year if row[5] else None

        offices.append(result_dict)

    person = CorpParty.query.filter(CorpParty.corp_party_id == int(corppartyid)).one()

    # one or both addr may be null, handle each case.
    if person.delivery_addr_id or person.mailing_addr_id:
        if person.delivery_addr_id and person.mailing_addr_id:
            expr = (CorpParty.delivery_addr_id == person.delivery_addr_id) | \
                (CorpParty.mailing_addr_id == person.mailing_addr_id)
        elif person.delivery_addr_id:
            expr = (CorpParty.delivery_addr_id == person.delivery_addr_id)
        elif person.mailing_addr_id:
            expr = (CorpParty.mailing_addr_id == person.mailing_addr_id)

        same_addr = (
            CorpParty.query
            .join(Event, Event.event_id == CorpParty.start_event_id)
            .add_columns(Event.event_timestmp)
            .filter(expr)
        )
    else:
        same_addr = []

    same_name_and_company = (
        CorpParty.query
        .join(Event, Event.event_id == CorpParty.start_event_id)
        .add_columns(Event.event_timestmp)
    )

    if person.first_nme:
        same_name_and_company = same_name_and_company.filter(
            CorpParty.first_nme.ilike(person.first_nme))

    if person.last_nme:
        same_name_and_company = same_name_and_company.filter(
            CorpParty.last_nme.ilike(person.last_nme))

    if person.corp_num:
        same_name_and_company = same_name_and_company.filter(
            CorpParty.corp_num.ilike(person.corp_num))

    return jsonify({
        'offices': offices,
        'same_addr': [
            {**s[0].as_dict(), **{'year': int(s[1].year)}} for s in same_addr if
            s[0].corp_party_id != int(corppartyid)],
        'same_name_and_company': [
            {**s[0].as_dict(), **{'year': int(s[1].year)}} for s in same_name_and_company if
            s[0].corp_party_id != int(corppartyid)],
    })


def _get_state_typ_cd_display_value(state_typ_cd):
    if state_typ_cd == STATE_TYP_CD_ACT:
        return STATE_TYP_CD_ACT
    else:
        return STATE_TYP_CD_HIS
