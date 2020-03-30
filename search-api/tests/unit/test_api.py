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

import copy
import json
from unittest.mock import patch

from tests.utilities.factory_utils import factory_auth_header
from tests.utilities.factory_scenarios import TestJwtClaims, JWT_HEADER
from search_api import status as http_status


def _dir_search(client, jwt, session, params):
    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.no_role)

    rv = client.get('/api/v1/directors/search/{}'.format(params),
                    headers=headers, content_type='application/json')

    assert rv.status_code == http_status.HTTP_200_OK
    return json.loads(rv.data)


def test_search_directors_sort(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that directors can be searched via GET."""

    dictionary = _dir_search(client, jwt, session, '?field=first_nme&operator=contains&value=a&mode=ALL&page=1&sort_type=asc&sort_value=middle_nme')
    assert len(dictionary['results']) == 20
    assert dictionary['results'][0]['middle_nme'] == 'Black'


def test_search_directors_first_nme_exact(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that directors can be searched via GET."""

    dictionary = _dir_search(client, jwt, session, '?field=first_nme&operator=exact&value=Lillian&mode=ALL&page=1&sort_type=asc&sort_value=last_nme')
    assert len(dictionary['results']) == 1
    assert dictionary['results'][0]['middle_nme'] == 'Black'

def test_search_directors_addr(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that directors can be searched via GET."""

    dictionary = _dir_search(client, jwt, session, '?field=addr_line_1&operator=contains&value=131%20Rue%20North&mode=ALL&page=1&sort_type=dsc&sort_value=last_nme')
    assert len(dictionary['results']) == 2
    assert dictionary['results'][0]['last_nme'] == 'Reeves'


def test_search_directors_any_nme(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that directors can be searched via GET."""

    dictionary = _dir_search(client, jwt, session, '?field=any_nme&operator=contains&value=black&mode=ALL&page=1&sort_type=dsc&sort_value=last_nme')
    assert len(dictionary['results']) == 4
    assert dictionary['results'][0]['last_nme'] == 'Marsh'

def test_search_directors_any_postal_cde(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that directors can be searched via GET."""

    dictionary = _dir_search(client, jwt, session, '?field=postal_cd&operator=exact&value=H2B%202X7&mode=ALL&page=1&sort_type=dsc&sort_value=last_nme')
    assert len(dictionary['results']) == 2
    assert dictionary['results'][0]['last_nme'] == 'Mcgee'


def test_search_corporations(client, jwt, session):
    """Check the offices-held service."""

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.no_role)

    rv = client.get('/api/v1/businesses/search/?query=1234567890&page=1&sort_type=dsc&sort_value=corp_nme',
                    headers=headers, content_type='application/json')

    assert rv.status_code == http_status.HTTP_200_OK

    dictionary = json.loads(rv.data)
    
    assert dictionary['results'][0]['corp_num'] == '1234567890'

    assert len(dictionary) == 1


def test_search_corporations_name(client, jwt, session):
    """Check the offices-held service."""

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.no_role)

    rv = client.get('/api/v1/businesses/search/?query=pembina&page=1&sort_type=dsc&sort_value=corp_nme',
                    headers=headers, content_type='application/json')

    assert rv.status_code == http_status.HTTP_200_OK

    dictionary = json.loads(rv.data)
    
    assert dictionary['results'][0]['corp_num'] == '1234567890'

    assert len(dictionary) == 1


def test_get_director(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that a director can be retrieved via GET."""

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.no_role)
    rv = client.get('/api/v1/directors/22',
                    headers=headers, content_type='application/json')

    assert rv.status_code == http_status.HTTP_200_OK
    dictionary = json.loads(rv.data)
    example = {
        'corp_admin_email': None,
        'corp_delivery_addr': "PO Box 273, Beiseker, AB",
        'corp_mailing_addr': "PO Box 273, Beiseker, AB",
        'corp_nme': "Bank of Montreal",
        'corp_num': "3756789012",
        'corp_party_email': None,
        'corp_party_id': 22,
        'corp_typ_cd': "A",
        'delivery_addr': "PO Box 273, Beiseker, AB",
        'first_nme': "Iarslov",
        'full_desc': "Notice of Change of Address",
        'last_nme': "Steele",
        'mailing_addr': "PO Box 273, Beiseker, AB",
        'middle_nme': None,
        'party_typ_cd': "DIR"}

    for k,v in example.items():
        assert dictionary[k] == v

def test_get_director_officesheld(client, jwt, session):
    """Check the offices-held service."""

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.no_role)

    rv = client.get('/api/v1/directors/officesheld/22',
                    headers=headers, content_type='application/json')

    assert rv.status_code == http_status.HTTP_200_OK

    dictionary = json.loads(rv.data)

    assert 'offices' in dictionary
    assert 'same_addr' in dictionary
    assert 'same_name_and_company' in dictionary

def test_search_directors(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that directors can be searched via GET."""

    dictionary = _dir_search(client, jwt, session, '?field=first_nme&operator=contains&value=a&mode=ALL&page=1&sort_type=dsc&sort_value=last_nme')
    assert len(dictionary['results']) == 20

    example = {'addr': 'PO Box 273', 'appointment_dt': 'Sun, 20 Oct 2019 00:00:00 GMT', 'cessation_dt': 'Sun, 20 Oct 2019 00:00:00 GMT', 'corp_nme': 'Bank of Montreal', 'corp_num': '3756789012', 'corp_party_id': 22, 'first_nme': 'Iarslov', 'last_nme': 'Steele', 'middle_nme': None, 'party_typ_cd': 'DIR', 'postal_cd': 'T0M 0G0', 'state_typ_cd': 'ACT'}
    for k,v in example.items():
        assert dictionary['results'][0][k] == v


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
