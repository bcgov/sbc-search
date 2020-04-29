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
"""Auth check and database warm-up endpoint."""
from http import HTTPStatus

from flask import jsonify, request, Blueprint, current_app
from sqlalchemy import exc

from search_api.auth import authorized, jwt
from search_api.models.base import db

API = Blueprint('AUTH_API', __name__, url_prefix='/api/v1/auth-check')


@API.route('/')
@jwt.requires_auth
def auth_check():
    """Check for authentication, and also warm up the database."""
    account_id = request.headers.get('X-Account-Id', None)
    if not authorized(jwt, account_id):
        return (
            jsonify({'message': 'User is not authorized to access Director Search'}),
            HTTPStatus.UNAUTHORIZED,
        )

    # Include a database health check at this point, because it greatly improves query
    # perf in the next minute or so, if the database is warmed up.
    try:
        if current_app.config.get('IS_ORACLE'):
            db.engine.execute('SELECT 1 FROM CORP_PARTY WHERE ROWNUM = 1')
        else:
            db.engine.execute('SELECT 1')
    except exc.SQLAlchemyError:
        return {'message': 'authorized, but api is down'}, HTTPStatus.SERVICE_UNAVAILABLE

    # made it here, so all checks passed
    return {'message': 'authorized, api is healthy'}, HTTPStatus.OK
