# Copyright © 2019 Province of British Columbia
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

"""Tests to verify the entities API end-point.

Test-Suite to ensure that the /entities endpoint is working as expected.
"""

import json
from unittest.mock import patch

from tests.utilities.factory_utils import factory_auth_header
from tests.utilities.factory_scenarios import TestJwtClaims
from search_api import status as http_status


def _dir_search(client, jwt, session, params):
    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.no_role)

    rv = client.get('/api/v1/directors/{}'.format(params),
                    headers=headers, content_type='application/json')

    assert rv.status_code == http_status.HTTP_200_OK
    return json.loads(rv.data)


def test_search_directors_sort(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that directors can be searched via GET."""

    dictionary = _dir_search(
        client, jwt, session,
        '?field=firstNme&operator=contains&value=a&mode=ALL&page=1&sort_type=asc&'
        'sort_value=middleNme&additional_cols=none')
    assert len(dictionary['results']) == 24
    assert dictionary['results'][0]['middleNme'] == 'Black'


def test_search_directors_firstNme_exact(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that directors can be searched via GET."""

    dictionary = _dir_search(
        client, jwt, session,
        '?field=firstNme&operator=exact&value=Lillian&mode=ALL&page=1&sort_type=asc&'
        'sort_value=lastNme&additional_cols=none')
    assert len(dictionary['results']) == 1
    assert dictionary['results'][0]['middleNme'] == 'Black'


def test_search_directors_addr(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that directors can be searched via GET."""

    dictionary = _dir_search(
        client, jwt, session,
        '?field=addr&operator=contains&value=131%20Rue%20North&mode=ALL&page=1&sort_type=dsc&'
        'sort_value=lastNme&additional_cols=addr')
    assert len(dictionary['results']) == 2
    assert 'lastNme' in dictionary['results'][0]


def test_search_directors_anyNme(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that directors can be searched via GET."""

    dictionary = _dir_search(
        client, jwt, session,
        '?field=anyNme&operator=contains&value=black&mode=ALL&page=1&sort_type=dsc&'
        'sort_value=lastNme&additional_cols=none')
    assert len(dictionary['results']) == 3


def test_search_directors_any_postal_code(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that directors can be searched via GET."""

    # search for postal code with a space in the middle
    dictionary = _dir_search(
        client, jwt, session,
        '?field=postalCd&operator=exact&value=H2B%202X7&mode=ALL&page=1&sort_type=dsc&'
        'sort_value=lastNme&additional_cols=addr')
    assert len(dictionary['results']) == 2

    # search for postal code without a space in the middle
    dictionary = _dir_search(
        client, jwt, session,
        '?field=postalCd&operator=exact&value=H2B2X7&mode=ALL&page=1&sort_type=dsc&'
        'sort_value=lastNme&additional_cols=addr')
    assert len(dictionary['results']) == 2


def test_search_corporations(client, jwt, session):
    """Check the offices-held service."""

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.no_role)

    rv = client.get('/api/v1/businesses/?query=1234567890&page=1&sort_type=dsc&sort_value=corpNme',
                    headers=headers, content_type='application/json')

    assert rv.status_code == http_status.HTTP_200_OK

    dictionary = json.loads(rv.data)

    assert dictionary['results'][0]['corpNum'] == '1234567890'

    assert len(dictionary) == 1


def test_search_corporations_name(client, jwt, session):
    """Check the offices-held service."""

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.no_role)

    rv = client.get('/api/v1/businesses/?query=pembina&page=1&sort_type=dsc&sort_value=corpNme',
                    headers=headers, content_type='application/json')

    assert rv.status_code == http_status.HTTP_200_OK

    dictionary = json.loads(rv.data)

    assert dictionary['results'][0]['corpNum'] == '1234567890'

    assert len(dictionary) == 1


def test_get_director(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that a director can be retrieved via GET."""

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.no_role)
    rv = client.get('/api/v1/directors/22',
                    headers=headers, content_type='application/json')

    assert rv.status_code == http_status.HTTP_200_OK
    dictionary = json.loads(rv.data)
    example = {
        'corpAdminEmail': None,
        'corpDeliveryAddr': "PO Box 273, Beiseker, AB",
        'corpMailingAddr': "PO Box 273, Beiseker, AB",
        'corpNme': "Bank of Montreal",
        'corpNum': "3756789012",
        'corpPartyEmail': None,
        'corpPartyId': 22,
        'corpTypCd': "A",
        'deliveryAddr': "PO Box 273, Beiseker, AB",
        'firstNme': "Iarslov",
        'fullDesc': "Notice of Change of Address",
        'lastNme': "Steele",
        'mailingAddr': "PO Box 273, Beiseker, AB",
        'middleNme': None,
        'partyTypCd': "DIR"}

    # The exact record above may differ depending on IDs, verify just the field names.
    for k, v in example.items():
        assert k in dictionary


def test_get_director_officesheld(client, jwt, session):
    """Check the offices-held service."""

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.no_role)

    rv = client.get('/api/v1/directors/22/offices',
                    headers=headers, content_type='application/json')

    assert rv.status_code == http_status.HTTP_200_OK

    dictionary = json.loads(rv.data)

    assert 'offices' in dictionary
    assert 'sameAddr' in dictionary
    assert 'sameNameAndCompany' in dictionary


def test_search_directors(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that directors can be searched via GET."""

    dictionary = _dir_search(
        client, jwt, session,
        '?field=firstNme&operator=contains&value=a&mode=ALL&page=1&sort_type=dsc&'
        'sort_value=lastNme&&additional_cols=addr')
    assert len(dictionary['results']) == 24

    example = {
        'addr': 'PO Box 273', 'appointmentDt': 'Sun, 20 Oct 2019 00:00:00 GMT',
        'cessationDt': 'Sun, 20 Oct 2019 00:00:00 GMT', 'corpNme': 'Bank of Montreal',
        'corpNum': '3756789012', 'corpPartyId': 22, 'firstNme': 'Iarslov', 'lastNme': 'Steele',
        'middleNme': None, 'partyTypCd': 'DIR', 'postalCd': 'T0M 0G0'}

    for k, v in example.items():
        assert k in dictionary['results'][0]


'''
def test_get_corporation_unauthorized_user_returns_403(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that an corporation can be retrieved via GET."""
    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.system_role)
    client.post('/api/v1/entities', data=json.dumps(TestEntityInfo.corporation1),
                headers=headers, content_type='application/json')

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.edit_role)

    rv = client.get('/api/v1/entities/{}'.format(TestEntityInfo.corporation1['businessIdentifier']),
                    headers=headers, content_type='application/json')

    assert rv.status_code == http_status.HTTP_403_FORBIDDEN


def test_get_corporation_no_auth_returns_401(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that an corporation cannot be retrieved without an authorization header."""
    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.system_role)
    client.post('/api/v1/entities', data=json.dumps(TestEntityInfo.corporation1),
                headers=headers, content_type='application/json')
    rv = client.get('/api/v1/entities/{}'.format(TestEntityInfo.corporation1['businessIdentifier']),
                    headers=None, content_type='application/json')
    assert rv.status_code == http_status.HTTP_401_UNAUTHORIZED

'''
