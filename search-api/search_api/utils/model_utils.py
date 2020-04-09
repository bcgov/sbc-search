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

from search_api.constants import STATE_TYP_CD_ACT, STATE_TYP_CD_HIS
from search_api.utils.utils import convert_to_snake_case


def _merge_addr_fields(row):
    address = row.addr_line_1
    if row.addr_line_2:
        address += ", " + row.addr_line_2
    if row.addr_line_3:
        address += ", " + row.addr_line_3
    return address


def _is_addr_search(fields):
    return "addr_line_1" in fields or "postal_cd" in fields


def _get_model_by_field(field_name):
    # local import to prevent circular import
    from search_api.models.corp_party import CorpParty  # noqa
    from search_api.models.corporation import Corporation  # noqa
    from search_api.models.corp_name import CorpName  # noqa
    from search_api.models.address import Address  # noqa
    from search_api.models.corp_op_state import CorpOpState  # noqa

    if field_name in ['firstNme', 'middleNme', 'lastNme', 'appointmentDt', 'cessationDt', 'corpNum',
                      'corpPartyId', 'partyTypCd']:  # CorpParty fields
        return eval('CorpParty')
    elif field_name in ['corpNum', 'recognitionDts', 'corpTypCd']:  # Corporation fields
        return eval('Corporation')
    elif field_name in ['corpNme']:  # CorpName fields
        return eval('CorpName')
    elif field_name in ['addrLine_1', 'addrLine_2', 'addrLine_3', 'postalCd', 'city', 'province']:  # Address fields
        return eval('Address')
    elif field_name in ['stateTypCd']:
        return eval('CorpOpState')


def _is_field_string(field_name):
    if field_name in [
        'firstNme', 'middleNme', 'lastNme', 'corpNum', 'corpPartyId', 'partyTypCd', 'corpTypCd',
            'corpNme', 'addrLine1', 'addrLine2', 'addrLine3', 'postalCd', 'city', 'province', 'stateTypCd']:
        return True
    else:
        return False


def _get_filter(field, operator, value):

    if field == 'anyNme':
        return (
            _get_filter('firstNme', operator, value) |
            _get_filter('middleNme', operator, value) |
            _get_filter('lastNme', operator, value))

    if field == 'addr':
        # Snake case converter doesn't add the underscores indicated below, so add it here so
        # the db field is correctly named after conversion.
        return (
            _get_filter('addrLine_1', operator, value) |
            _get_filter('addrLine_2', operator, value) |
            _get_filter('addrLine_3', operator, value))

    if field == 'stateTypCd':
        # state_typ_cd is either "ACT", or displayed as "HIS" for any other value
        if value == STATE_TYP_CD_ACT:
            operator = 'exact'
        elif value == STATE_TYP_CD_HIS:
            operator = 'excludes'
            value = STATE_TYP_CD_ACT

    model = _get_model_by_field(field)

    value = value.lower()
    if model:
        Field = getattr(model, convert_to_snake_case(field))
        # TODO: we should sanitize the values
        if operator == 'contains':
            return Field.ilike('%' + value + '%')
        elif operator == 'exact':
            return Field.ilike(value)
        elif operator == 'endswith':
            return Field.ilike('%' + value)
        elif operator == 'startswith':
            return Field.ilike(value + '%')
        elif operator == 'wildcard':
            # We support entering * or % as wildcards, but the actual wildcard is %
            value = value.replace("*", "%")
            return Field.ilike(value)
        elif operator == 'excludes':
            return ~Field.ilike(value)
        else:
            raise Exception('invalid operator: {}'.format(operator))
    else:
        raise Exception('invalid field: {}'.format(field))


def _get_sort_field(field_name):

    model = _get_model_by_field(field_name)
    if model:
        return getattr(model, convert_to_snake_case(field_name))
    else:
        raise Exception('invalid sort field: {}'.format(field_name))


def _sort_by_field(sort_type, sort_value):
    field = _get_sort_field(sort_value)

    sort_field_str = "{field}".format(field=field)

    if _is_field_string(sort_value):
        sort_field_str = "func.lower({field})".format(field=sort_field_str)

    if sort_type == 'dsc':
        sort_field_str += ".desc()"

    return sort_field_str


def _format_office_typ_cd(office_typ_cd):
    if office_typ_cd == "RG":
        return "Registered"
    elif office_typ_cd == "RC":
        return "Records"
