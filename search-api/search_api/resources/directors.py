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
from http import HTTPStatus
import logging
from tempfile import NamedTemporaryFile

from flask import Blueprint, current_app, request, jsonify, send_from_directory
from openpyxl import Workbook

from search_api.auth import jwt, authorized
from search_api.constants import ADDITIONAL_COLS_ADDRESS, ADDITIONAL_COLS_ACTIVE, STATE_TYP_CD_ACT, STATE_TYP_CD_HIS
from search_api.models.address import Address
from search_api.models.corp_state import CorpState
from search_api.models.corp_party import CorpParty
from search_api.models.corp_name import CorpName
from search_api.models.office import Office
from search_api.utils.model_utils import (
    _merge_addr_fields,
    _is_addr_search,
    BadSearchValue
)
from search_api.utils.utils import convert_to_snake_case

logger = logging.getLogger(__name__)
API = Blueprint('DIRECTORS_API', __name__, url_prefix='/api/v1/directors')


@API.route('/')

def corpparty_search():
    current_app.logger.info("Starting director search")

    account_id = request.headers.get("X-Account-Id", None)
    
    current_app.logger.info("Authorization check finished; starting query {query}".format(query=request.url))

    args = request.args
    fields = args.getlist('field')
    additional_cols = args.get('additional_cols')
    try:
        results = CorpParty.search_corp_parties(args)
    except BadSearchValue as e:
        return {
            'results': [],
            'error': 'Invalid search: {}'.format(str(e))
        }

    current_app.logger.info("Before query")

    # Pagination
    page = int(args.get("page")) if "page" in args else 1

    per_page = 50
    # Manually paginate results, because flask-sqlalchemy's paginate() method counts the total,
    # which is slow for large tables. This has been addressed in flask-sqlalchemy but is unreleased.
    # Ref: https://github.com/pallets/flask-sqlalchemy/pull/613
    results = results.limit(per_page).offset((page - 1) * per_page)

    # for benchmarking, dump the query here and copy to benchmark.py
    # from sqlalchemy.dialects import oracle
    # oracle_dialect = oracle.dialect(max_identifier_length=30)
    # raise Exception(results.statement.compile(dialect=oracle_dialect))

    current_app.logger.info("After query")

    corp_parties = []
    for row in results:
        result_fields = [
            'corpPartyId', 'firstNme', 'middleNme', 'lastNme', 'appointmentDt', 'cessationDt',
            'corpNum', 'corpNme', 'partyTypCd']
        result_dict = {key: getattr(row, convert_to_snake_case(key)) for key in result_fields}
        result_dict['corpPartyId'] = int(result_dict['corpPartyId'])

        CorpParty.add_additional_cols_to_search_results(additional_cols, fields, row, result_dict)

        corp_parties.append(result_dict)

    current_app.logger.info("Returning JSON results")

    return jsonify({'results': corp_parties})


@API.route('/export/')
@jwt.requires_auth
def corpparty_search_export():
    account_id = request.headers.get("X-Account-Id", None)
    if not authorized(jwt, account_id):
        return jsonify({'message': 'User is not authorized to access Director Search'}), HTTPStatus.UNAUTHORIZED

    # Query string arguments
    args = request.args
    fields = args.getlist('field')
    additional_cols = args.get('additional_cols')

    # Fetching results
    results = CorpParty.search_corp_parties(args)

    # Exporting to Excel
    wb = Workbook()

    export_dir = "/tmp"
    with NamedTemporaryFile(mode='w+b', dir=export_dir, delete=True):

        sheet = wb.active

        # Sheet headers (first row)
        column_headers = [
            "Filing #", "Surname", "First Name", "Middle Name",
            "Office Held", "Appointed", "Ceased", "Company Name", "Inc/Reg #"]
        if _is_addr_search(fields) or additional_cols == ADDITIONAL_COLS_ADDRESS:
            column_headers.insert(4, "Address")
            column_headers.insert(5, "Postal Code")
        elif additional_cols == ADDITIONAL_COLS_ACTIVE:
            column_headers.insert(7, "Company Status")

        for index, column_header in enumerate(column_headers, start=1):
            _ = sheet.cell(column=index, row=1, value=column_header)

        for row_index, row in enumerate(results, start=2):
            columns = [
                row.corp_party_id, row.last_nme, row.first_nme, row.middle_nme, row.party_typ_cd,
                row.appointment_dt, row.cessation_dt, row.corp_nme, row.corp_num]

            if _is_addr_search(fields) or additional_cols == ADDITIONAL_COLS_ADDRESS:
                columns.insert(4, _merge_addr_fields(row))
                columns.insert(5, row.postal_cd)
            elif additional_cols == ADDITIONAL_COLS_ACTIVE:
                columns.insert(7, _get_state_typ_cd_display_value(row.state_typ_cd))

            for column_index, column_value in enumerate(columns, start=1):
                _ = sheet.cell(column=column_index, row=row_index, value=column_value)

        current_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
        filename = "Director Search Results {date}.xlsx".format(date=current_date)
        full_filename_path = "{dir}/{filename}".format(dir=export_dir, filename=filename)
        wb.save(filename=full_filename_path)

        return send_from_directory(export_dir, filename, as_attachment=True)


@API.route('/<id>')
@jwt.requires_auth
def person(id):
    account_id = request.headers.get("X-Account-Id", None)
    if not authorized(jwt, account_id):
        return jsonify({'message': 'User is not authorized to access Director Search'}), HTTPStatus.UNAUTHORIZED

    result = CorpParty.get_corporation_info_by_corp_party_id(id)

    person = result[0]
    result_dict = {}

    filing_description = CorpParty.get_filing_description_by_corp_party_id(id)

    name = CorpName.get_corp_name_by_corp_id(person.corp_num)[0]
    offices = Office.get_offices_by_corp_id(person.corp_num)
    delivery_addr = Address.normalize_addr(person.delivery_addr_id)
    mailing_addr = Address.normalize_addr(person.mailing_addr_id)

    states = CorpState.get_corp_states_by_corp_id(person.corp_num)

    corp_delivery_addr = ';'.join([Address.normalize_addr(office.delivery_addr_id) for office in offices])
    corp_mailing_addr = ';'.join([Address.normalize_addr(office.mailing_addr_id) for office in offices])

    result_dict['corpPartyId'] = int(person.corp_party_id)
    result_dict['firstNme'] = person.first_nme
    result_dict['middleNme'] = person.middle_nme
    result_dict['lastNme'] = person.last_nme
    result_dict['appointmentDt'] = person.appointment_dt
    result_dict['cessationDt'] = person.cessation_dt
    result_dict['corpNum'] = person.corp_num
    result_dict['corpNme'] = name.corp_nme
    result_dict['partyTypCd'] = person.party_typ_cd
    result_dict['corpPartyEmail'] = person.email_address
    result_dict['deliveryAddr'] = delivery_addr
    result_dict['mailingAddr'] = mailing_addr
    result_dict['corpDeliveryAddr'] = corp_delivery_addr
    result_dict['corpMailingAddr'] = corp_mailing_addr
    result_dict['corpTypCd'] = result.corp_typ_cd
    result_dict['corpAdminEmail'] = result.admin_email
    result_dict['fullDesc'] = filing_description[0].full_desc if filing_description else None

    result_dict['states'] = [s.as_dict() for s in states]

    return jsonify(result_dict)


@API.route('/<corppartyid>/offices')
@jwt.requires_auth
def officesheld(corppartyid):
    account_id = request.headers.get("X-Account-Id", None)
    if not authorized(jwt, account_id):
        return jsonify({'message': 'User is not authorized to access Director Search'}), HTTPStatus.UNAUTHORIZED

    results = CorpParty.get_offices_held_by_corp_party_id(corppartyid)
    offices = []
    for row in results:
        result_dict = {}

        result_dict['corpPartyId'] = int(row.corp_party_id)
        result_dict['officerTypCd'] = row.officer_typ_cd
        result_dict['shortDesc'] = row.short_desc
        result_dict['appointmentDt'] = row.appointment_dt
        result_dict['year'] = row.event_timestmp.year if row.event_timestmp else None

        offices.append(result_dict)

    same_addr = CorpParty.get_corp_party_at_same_addr(corppartyid)
    same_name_and_company = CorpParty.get_corp_party_same_name_at_same_addr(corppartyid)

    return jsonify({
        'offices': offices,
        'sameAddr': [
            {**s[0].as_dict(), **{'year': int(s[1].year)}} for s in same_addr if
            s[0].corp_party_id != int(corppartyid)],
        'sameNameAndCompany': [
            {**s[0].as_dict(), **{'year': int(s[1].year)}} for s in same_name_and_company if
            s[0].corp_party_id != int(corppartyid)],
    })


def _get_state_typ_cd_display_value(state_typ_cd):
    if state_typ_cd == STATE_TYP_CD_ACT:
        return STATE_TYP_CD_ACT
    else:
        return STATE_TYP_CD_HIS
