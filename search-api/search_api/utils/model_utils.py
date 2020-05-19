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

from flask import current_app
from sqlalchemy import func, literal_column

from search_api.constants import STATE_TYP_CD_ACT, STATE_TYP_CD_HIS, ADDITIONAL_COLS_ADDRESS, ADDITIONAL_COLS_ACTIVE
from search_api.utils.utils import convert_to_snake_case
from search_api.models.nickname import NickName


def _merge_addr_fields(row):
    address = row.addr_line_1
    if row.addr_line_2:
        address += ', ' + row.addr_line_2
    if row.addr_line_3:
        address += ', ' + row.addr_line_3
    try:
        address += ', ' + row.city
    except:
        pass
    return address


def _is_addr_search(fields):
    return 'addrLine1' in fields or 'addr' in fields or 'postalCd' in fields


def _get_model_by_field(field_name):
    # local import to prevent circular import
    from search_api.models.corp_party import CorpParty  # noqa # pylint: disable=import-outside-toplevel, unused-import, cyclic-import
    from search_api.models.corporation import Corporation  # noqa # pylint: disable=import-outside-toplevel, unused-import, cyclic-import
    from search_api.models.corp_name import CorpName  # noqa # pylint: disable=import-outside-toplevel, unused-import
    from search_api.models.address import Address  # noqa # pylint: disable=import-outside-toplevel, unused-import
    from search_api.models.corp_state import CorpState  # noqa # pylint: disable=import-outside-toplevel, unused-import

    if field_name in ['firstNme', 'middleNme', 'lastNme', 'appointmentDt', 'cessationDt',
                      'corpPartyId', 'partyTypCd']:  # CorpParty fields
        return CorpParty
    if field_name in ['corpNum', 'recognitionDts', 'corpTypCd']:  # Corporation fields
        return Corporation
    if field_name in ['corpNme']:  # CorpName fields
        return CorpName
    if field_name in ['addrLine1', 'addrLine2', 'addrLine3', 'postalCd', 'city', 'province']:  # Address fields
        return Address
    if field_name in ['stateTypCd']:
        return CorpState

    raise Exception('invalid field: {}'.format(field_name))


def _get_filter(field_name, operator, value, end_recursion=False):
    """Generate a SQL search expression given a filter specified by the user."""
    value = value.upper()

    if field_name == 'anyNme':
        return (
            _get_filter('firstNme', operator, value) |
            _get_filter('middleNme', operator, value) |
            _get_filter('lastNme', operator, value))

    # This currently hangs, so we never call it from the front-end.
    # It seems a boolean OR with multiple CONTAINS() calls in Oracle does not resolve currently.
    if field_name == 'addr':
        # We expect the building number and street name '123 main' to be in line 1 or 2 of the address.
        return (
            _get_filter('addrLine1', 'text', value) |
            _get_filter('addrLine2', 'text', value))

    # Enforce text search only on addresses.
    if 'addrLine' in field_name:
        operator = 'text'

    if field_name == 'stateTypCd':
        # state_typ_cd is either 'ACT', or displayed as 'HIS' for any other value
        if value == STATE_TYP_CD_ACT:
            operator = 'exact'
        elif value == STATE_TYP_CD_HIS:
            operator = 'excludes'
            value = STATE_TYP_CD_ACT

    if field_name == 'postalCd' and not end_recursion:
        return (
            _get_filter('postalCd', 'exact', value[:3] + ' ' + value[3:6], True) |
            _get_filter('postalCd', 'exact', value, True))

    model = _get_model_by_field(field_name)

    if len(value) < 2:
        raise BadSearchValue('Search value must be at least 2 letters long.')

    if model:
        field = getattr(model, convert_to_snake_case(field_name))
        return _generate_field_filter(field, operator, value)

    raise Exception('invalid field: {}'.format(field_name))


def _generate_field_filter(field, operator, value):

    if operator == 'text':
        # On Oracle, allow indexed text search.
        if current_app.config.get('IS_ORACLE'):
            expr = func.contains(field, value) > literal_column('0')
        else:
            expr = func.upper(field).like('%' + value + '%')
    # Note: The Oracle back-end performs better with UPPER() compared to LOWER() case casting.
    elif operator == 'contains':
        expr = func.upper(field).like('%' + value + '%')
    elif operator == 'exact':
        expr = func.upper(field) == value
    elif operator == 'endswith':
        expr = func.upper(field).like('%' + value)
    elif operator == 'startswith':
        expr = func.upper(field).like(value + '%')
    elif operator == 'wildcard':
        # We support entering * or % as wildcards, but the actual wildcard is %
        value = value.replace('*', '%')
        expr = func.upper(field).like(value)
    elif operator == 'excludes':
        expr = func.upper(field) != value
        # TODO: this is a relatively expensive op, we may want to enforce it's only used in
        # combination with other queries.
        # TODO: we should consider sorting by similarity (sum of any filters using it) by
        # default, if the user chooses any similarity filter.
    elif operator == 'similar':
        expr = func.utl_match.jaro_winkler_similarity(field, value) > 85
    elif operator == 'nicknames':
        expr = NickName.get_nickname_search_expr(field, value)
    else:
        raise Exception('invalid operator: {}'.format(operator))

    return expr


def _get_sort_field(field_name):

    model = _get_model_by_field(field_name)
    if model:
        return getattr(model, convert_to_snake_case(field_name))

    raise Exception('invalid sort field: {}'.format(field_name))


def _sort_by_field(sort_type, sort_value):
    field = _get_sort_field(sort_value)

    # by convention, in our database, dates end with _dts or _dt (converted to snake case)
    if not sort_value.endswith('Dt') and not sort_value.endswith('Dts'):
        # Note: The Oracle back-end performs better with UPPER() compared to LOWER() case casting.
        field = func.upper(field)

    if sort_type == 'dsc':
        field = field.desc()
    return field


def _format_office_typ_cd(office_typ_cd):
    if office_typ_cd == 'RG':
        return 'Registered'
    if office_typ_cd == 'RC':  # pylint: disable=no-else-return
        return 'Records'

    return ''


class BadSearchValue(Exception):
    """Exception class for invalid search queries."""

    pass  # pylint: disable=unnecessary-pass


def _get_state_typ_cd_display_value(state_typ_cd):
    if state_typ_cd == STATE_TYP_CD_ACT:
        return STATE_TYP_CD_ACT

    return STATE_TYP_CD_HIS


def _get_corp_party_export_column_headers(args):
    fields = args.getlist('field')
    additional_cols = args.get('additional_cols')

    column_headers = [
        'Surname', 'First Name', 'Middle Name', 'Office Held', 'Appointed', 'Ceased',
        'Company Name', 'Inc/Reg #']
    if _is_addr_search(fields) or additional_cols == ADDITIONAL_COLS_ADDRESS:
        column_headers.insert(3, 'Address')
        column_headers.insert(4, 'Postal Code')

    if additional_cols == ADDITIONAL_COLS_ACTIVE:
        column_headers.insert(6, 'Company Status')

    return column_headers


def _get_corp_party_export_column_values(row, args):
    fields = args.getlist('field')
    additional_cols = args.get('additional_cols')

    columns = [
        row.last_nme, row.first_nme, row.middle_nme, row.party_typ_cd,
        row.appointment_dt, row.cessation_dt, row.corp_nme, row.corp_num]

    if _is_addr_search(fields) or additional_cols == ADDITIONAL_COLS_ADDRESS:
        columns.insert(3, _merge_addr_fields(row))
        columns.insert(4, row.postal_cd)

    if additional_cols == ADDITIONAL_COLS_ACTIVE:
        columns.insert(6, _get_state_typ_cd_display_value(row.state_typ_cd))

    return columns
