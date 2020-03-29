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

def test_get_corporation(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that an corporation can be retrieved via GET."""
    headers_system = factory_auth_header(jwt=jwt, claims=TestJwtClaims.system_role)
    rv_create = client.post('/api/v1/entities', data=json.dumps(TestEntityInfo.corporation1),
                            headers=headers_system, content_type='application/json')
    assert rv_create.status_code == http_status.HTTP_201_CREATED

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.passcode)

    rv = client.get('/api/v1/entities/{}'.format(TestEntityInfo.corporation1['businessIdentifier']),
                    headers=headers, content_type='application/json')

    assert rv.status_code == http_status.HTTP_200_OK
    dictionary = json.loads(rv.data)
    assert dictionary['businessIdentifier'] == TestEntityInfo.corporation1['businessIdentifier']

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
