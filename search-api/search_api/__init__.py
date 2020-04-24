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
"""Search API service."""

import logging
import os
from datetime import date

from flask.json import JSONEncoder
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from sbc_common_components.utils.camel_case_response import convert_to_camel
from search_api.config import _Config, CONFIGURATION
from search_api.auth import jwt
from search_api.resources import DIRECTORS_API, BUSINESSES_API, OPS_API, AUTH_API
from search_api.models.base import db
from search_api.utils.util_logging import setup_logging

load_dotenv(verbose=True)

setup_logging(os.path.join(_Config.PROJECT_ROOT, 'logging.conf'))  # important to do this first


class CustomJSONEncoder(JSONEncoder):
    """encode dates as ISO8601."""

    def default(self, obj):  # pylint: disable=method-hidden, arguments-differ
        """Override date formatting."""
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def create_app(run_mode=os.getenv('FLASK_ENV', 'production')):
    """Return a configured Flask App using the Factory method."""
    app = Flask(__name__)
    app.config.from_object(CONFIGURATION[run_mode])
    app.logger.setLevel(logging.INFO)  # pylint: disable=no-member

    db.init_app(app)
    app.json_encoder = CustomJSONEncoder

    if app.debug:
        migrate = Migrate(app, db)  # noqa # pylint: disable=unused-variable

    CORS(app)

    # Configure Sentry
    if app.config.get('SENTRY_DSN', None):
        sentry_sdk.init(
            dsn=app.config.get('SENTRY_DSN'), integrations=[FlaskIntegration()]
        )

    app.register_blueprint(DIRECTORS_API)
    app.register_blueprint(BUSINESSES_API)
    app.register_blueprint(OPS_API)
    app.register_blueprint(AUTH_API)
    app.after_request(convert_to_camel)

    if not app.config.get('BENCHMARK', None):
        setup_jwt_manager(app, jwt)

    return app


def setup_jwt_manager(app, jwt_manager):
    """Use flask app to configure the JWTManager to work for a particular Realm."""
    def get_roles(a_dict):
        return a_dict['realm_access']['roles']  # pragma: no cover
    app.config['JWT_ROLE_CALLBACK'] = get_roles

    jwt_manager.init_app(app)
