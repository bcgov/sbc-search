# Copyright © 2020 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This module holds utility functions related to model fields and serialization."""

from sqlalchemy import func

from search_api.constants import STATE_TYP_CD_ACT, STATE_TYP_CD_HIS, ADDITIONAL_COLS_ADDRESS, ADDITIONAL_COLS_ACTIVE
from search_api.utils.utils import convert_to_snake_case


def _merge_addr_fields(row):
    address = row.addr_line_1
    if row.addr_line_2:
        address += ', ' + row.addr_line_2
    if row.addr_line_3:
        address += ', ' + row.addr_line_3
    return address


def _is_addr_search(fields):
    return 'addr_line_1' in fields or 'postal_cd' in fields


def _get_model_by_field(field_name):
    # local import to prevent circular import
    from search_api.models.corp_party import CorpParty  # noqa # pylint: disable=import-outside-toplevel, unused-import, cyclic-import
    from search_api.models.corporation import Corporation  # noqa # pylint: disable=import-outside-toplevel, unused-import, cyclic-import
    from search_api.models.corp_name import CorpName  # noqa # pylint: disable=import-outside-toplevel, unused-import
    from search_api.models.address import Address  # noqa # pylint: disable=import-outside-toplevel, unused-import
    from search_api.models.corp_op_state import CorpOpState  # noqa # pylint: disable=import-outside-toplevel, unused-import

    if field_name in ['firstNme', 'middleNme', 'lastNme', 'appointmentDt', 'cessationDt', 'corpNum',
                      'corpPartyId', 'partyTypCd']:  # CorpParty fields
        return eval('CorpParty')  # pylint: disable=eval-used
    if field_name in ['corpNum', 'recognitionDts', 'corpTypCd']:  # Corporation fields
        return eval('Corporation')  # pylint: disable=eval-used
    if field_name in ['corpNme']:  # CorpName fields
        return eval('CorpName')  # pylint: disable=eval-used
    if field_name in ['addrLine1', 'addrLine2', 'addrLine3', 'postalCd', 'city', 'province']:  # Address fields
        return eval('Address')  # pylint: disable=eval-used
    if field_name in ['stateTypCd']:
        return eval('CorpOpState')  # pylint: disable=eval-used

    raise Exception('invalid field: {}'.format(field_name))


def _is_field_string(field_name):
    if field_name in [
            'firstNme', 'middleNme', 'lastNme', 'corpNum', 'corpPartyId', 'partyTypCd', 'corpTypCd',
            'corpNme', 'addrLine1', 'addrLine2', 'addrLine3', 'postalCd', 'city', 'province', 'stateTypCd']:
        return True

    return False


def _get_filter(field_name, operator, value):
    operator, value = _handle_field_special_cases(field_name, operator, value)

    model = _get_model_by_field(field_name)

    # Note: The Oracle back-end performs better with UPPER() compared to LOWER() case casting.
    value = value.upper()
    if model:
        field = getattr(model, convert_to_snake_case(field_name))
        # TODO: we should sanitize the values
        if operator == 'contains':
            return func.upper(field).ilike('%' + value + '%')
        if operator == 'exact':
            return func.upper(field) == value
        if operator == 'endswith':
            return func.upper(field).like('%' + value)
        if operator == 'startswith':
            return func.upper(field).like(value + '%')
        if operator == 'wildcard':
            # We support entering * or % as wildcards, but the actual wildcard is %
            value = value.replace('*', '%')
            return func.upper(field).like(value)
        if operator == 'excludes':
            return func.upper(field) != value

        raise Exception('invalid operator: {}'.format(operator))

    raise Exception('invalid field: {}'.format(field_name))


def _handle_field_special_cases(field_name, operator, value):
    if field_name == 'anyNme':
        return (
            _get_filter('firstNme', operator, value) |
            _get_filter('middleNme', operator, value) |
            _get_filter('lastNme', operator, value))

    if field_name == 'addr':
        return (
            _get_filter('addrLine1', operator, value) |
            _get_filter('addrLine2', operator, value) |
            _get_filter('addrLine3', operator, value))

    if field_name == 'stateTypCd':
        # state_typ_cd is either 'ACT', or displayed as 'HIS' for any other value
        if value == STATE_TYP_CD_ACT:
            operator = 'exact'
        elif value == STATE_TYP_CD_HIS:
            operator = 'excludes'
            value = STATE_TYP_CD_ACT

    if field_name == 'postalCd':
        # Search for postal codes with or without a space in the middle
        value = value[0:3] + '%' + value[3:6]
        operator = 'contains'

    return operator, value


def _get_sort_field(field_name):

    model = _get_model_by_field(field_name)
    if model:
        return getattr(model, convert_to_snake_case(field_name))

    raise Exception('invalid sort field: {}'.format(field_name))


def _sort_by_field(sort_type, sort_value):
    field = _get_sort_field(sort_value)

    sort_field_str = '{field}'.format(field=field)

    if _is_field_string(sort_value):
        # Note: The Oracle back-end performs better with UPPER() compared to LOWER() case casting.
        sort_field_str = 'func.upper({field})'.format(field=sort_field_str)

    if sort_type == 'dsc':
        sort_field_str += '.desc()'

    return sort_field_str


def _format_office_typ_cd(office_typ_cd):
    if office_typ_cd == 'RG':
        return 'Registered'
    if office_typ_cd == 'RC':  # pylint: disable=no-else-return
        return 'Records'

    return ''


def _get_state_typ_cd_display_value(state_typ_cd):
    if state_typ_cd == STATE_TYP_CD_ACT:
        return STATE_TYP_CD_ACT

    return STATE_TYP_CD_HIS


def _get_corp_party_export_column_headers(args):
    fields = args.getlist('field')
    additional_cols = args.get('additional_cols')

    column_headers = [
        'Filing #', 'Surname', 'First Name', 'Middle Name',
        'Office Held', 'Appointed', 'Ceased', 'Company Name', 'Inc/Reg #']
    if _is_addr_search(fields) or additional_cols == ADDITIONAL_COLS_ADDRESS:
        column_headers.insert(4, 'Address')
        column_headers.insert(5, 'Postal Code')
    elif additional_cols == ADDITIONAL_COLS_ACTIVE:
        column_headers.insert(7, 'Company Status')

    return column_headers


def _get_corp_party_export_column_values(row, args):
    fields = args.getlist('field')
    additional_cols = args.get('additional_cols')

    columns = [
        row.corp_party_id, row.last_nme, row.first_nme, row.middle_nme, row.party_typ_cd,
        row.appointment_dt, row.cessation_dt, row.corp_nme, row.corp_num]

    if _is_addr_search(fields) or additional_cols == ADDITIONAL_COLS_ADDRESS:
        columns.insert(4, _merge_addr_fields(row))
        columns.insert(5, row.postal_cd)
    elif additional_cols == ADDITIONAL_COLS_ACTIVE:
        columns.insert(7, _get_state_typ_cd_display_value(row.state_typ_cd))

    return columns
