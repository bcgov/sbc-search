# Copyright © 2019 Province of British Columbia
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
"""Endpoints to check and manage the health of the service."""
from flask import Blueprint, current_app
from sqlalchemy import exc
from http import HTTPStatus

from search_api.models.base import db


API = Blueprint('OPS', __name__, url_prefix='/ops')


@API.route('/readyz')
def readyz():
    """Return a JSON object that identifies if the service is ready."""
    return {'message': 'api is ready'}, HTTPStatus.OK


@API.route('/healthz')
def healthz():
    """Return a JSON object stating the health of the Service and dependencies."""
    try:
        if current_app.config.get("IS_ORACLE"):
            db.engine.execute('SELECT 1 FROM CORP_PARTY WHERE ROWNUM = 1')
        else:
            db.engine.execute('SELECT 1')
    except exc.SQLAlchemyError:
        return {'message': 'api is down'}, HTTPStatus.SERVICE_UNAVAILABLE

    # made it here, so all checks passed
    return {'message': 'api is healthy'}, HTTPStatus.OK
