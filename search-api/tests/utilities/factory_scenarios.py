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
"""Test Utils.

Test Utility for creating test scenarios.
"""
from enum import Enum


JWT_HEADER = {
    'alg': 'RS256',
    'typ': 'JWT',
    'kid': 'flask-jwt-oidc-test-client'
}


class TestJwtClaims(dict, Enum):
    """Test scenarios of jwt claims."""

    no_role = {
        'iss': 'https://example.localdomain/auth/realms/example',
        'aud': 'flask-jwt-oidc-test-client',
        'sub': 'f7a4a1d3-73a8-4cbc-a40f-bb1145302065',
        'firstname': 'Test',
        'lastname': 'User 2',
        'preferred_username': 'testuser2',
        'realm_access': {
            'roles': [
            ]
        }
    }

    invalid = {
        'sub': 'barfoo',
        'firstname': 'Trouble',
        'lastname': 'Maker',
        'preferred_username': 'troublemaker'
    }

    staff_role = {
        'iss': 'https://example.localdomain/auth/realms/example',
        'aud': 'flask-jwt-oidc-test-client',
        'sub': 'f7a4a1d3-73a8-4cbc-a40f-bb1145302064',
        'firstname': 'Test',
        'lastname': 'User',
        'preferred_username': 'testuser',
        'realm_access': {
            'roles': [
                'staff'
            ]
        }
    }

    system_role = {
        'iss': 'https://example.localdomain/auth/realms/example',
        'aud': 'flask-jwt-oidc-test-client',
        'sub': 'f7a4a1d3-73a8-4cbc-a40f-bb1145302064',
        'firstname': 'Test',
        'lastname': 'User',
        'preferred_username': 'testuser',
        'realm_access': {
            'roles': [
                'system'
            ]
        },
        'corp_type': 'CP'
    }

    @staticmethod
    def get_test_user(sub):
        """Return test user with subject from argument."""
        return {
            'iss': 'https://example.localdomain/auth/realms/example',
            'aud': 'flask-jwt-oidc-test-client',
            'sub': sub,
            'firstname': 'Test',
            'lastname': 'User',
            'preferred_username': 'CP1234567',
            'username': 'CP1234567',
            'realm_access': {
                'roles': [
                    'staff'
                ]
            },
            'loginSource': 'PASSCODE'
        }
