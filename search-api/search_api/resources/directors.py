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
    CorpState,
    CorpParty,
    CorpName,
    Office,
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
def corpparty_search():
    args = request.args
    results = _get_corpparty_search_results(args)

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
    result = CorpParty.get_corporation_info_by_corp_party_id(id)

    person = result[0]
    result_dict = {}

    filing_description = CorpParty.get_filing_description_by_corp_party_id(id)

    name = CorpName.get_corp_name_by_corp_id(person.corp_num)[0]
    offices = Office.get_offices_by_corp_id(person.corp_num)
    delivery_addr = _normalize_addr(person.delivery_addr_id)
    mailing_addr = _normalize_addr(person.mailing_addr_id)

    states = CorpState.get_corp_states_by_corp_id(person.corp_num)

    corp_delivery_addr = ';'.join([_normalize_addr(office.delivery_addr_id) for office in offices])
    corp_mailing_addr = ';'.join([_normalize_addr(office.mailing_addr_id) for office in offices])

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
    result_dict['corp_typ_cd'] = result.corp_typ_cd
    result_dict['corp_admin_email'] = result.admin_email
    result_dict['full_desc'] = filing_description[0].full_desc if filing_description else None

    result_dict['states'] = [s.as_dict() for s in states]

    return jsonify(result_dict)


@API.route('/officesheld/<corppartyid>')
@jwt.requires_auth
def officesheld(corppartyid):
    results = CorpParty.get_offices_held_by_corp_party_id(corppartyid)
    offices = []
    for row in results:
        result_dict = {}

        result_dict['corp_party_id'] = int(row.corp_party_id)
        result_dict['officer_typ_cd'] = row.officer_typ_cd
        result_dict['short_desc'] = row.short_desc
        result_dict['appointment_dt'] = row.appointment_dt
        result_dict['year'] = row.event_timestmp.year if row.event_timestmp else None

        offices.append(result_dict)

    same_addr = CorpParty.get_corp_party_at_same_addr(corppartyid)
    same_name_and_company = CorpParty.get_corp_party_same_name_at_same_addr(corppartyid)

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
