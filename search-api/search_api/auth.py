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
'''Authorization service for the Search API.'''

import json

from flask import current_app
from flask_jwt_oidc import JwtManager
import requests

jwt = JwtManager()  # pylint: disable=invalid-name


def authorized(jwt_instance, account_id):
    '''
    Assert that the user is authorized to access Director Search.

    The user should have an orgMembership in the Director Search (DIR_SEARCH) application.
    '''
    # When running tests, just mock out this entire user membership authorization check as it requires
    # an external service.

    if current_app.config['DEBUG'] or current_app.config['TESTING']:
        return True

    if not jwt_instance or not account_id:
        return False

    token = jwt_instance.get_token_auth_header()
    auth_api_url_base = current_app.config['AUTH_API_URL']
    auth_api_url = '{auth_api_url_base}/api/v1/accounts/{account_id}/products/DIR_SEARCH/authorizations'.format(
        auth_api_url_base=auth_api_url_base, account_id=account_id)

    headers = {'Authorization': 'Bearer {token}'.format(token=token)}
    response = requests.get(auth_api_url, headers=headers)

    try:
        response_json = response.json()
    except json.decoder.JSONDecodeError:
        raise Exception('Invalid JSON in auth rsp: `{}`'.format(response.text))

    if 'orgMembership' in response_json:
        return True

    return False
