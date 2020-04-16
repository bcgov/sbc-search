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
"""Super class to handle all operations related to base model."""


from decimal import Decimal

import flask.json
from flask_sqlalchemy import SQLAlchemy


class MyJSONEncoder(flask.json.JSONEncoder):
    """This class extends the default Flask JSON encoder."""

    def default(self, o):  # pylint: disable=method-hidden
        """Extend parent method and handle Decimal instances."""
        if isinstance(o, Decimal):
            # Convert decimal instances to strings.
            return str(o)
        return super(MyJSONEncoder, self).default(o)


flask.json_encoder = MyJSONEncoder
db = SQLAlchemy()  # pylint: disable=invalid-name


class BaseModel(db.Model):
    """This class manages all of the base model functions."""

    # pylint: disable=too-few-public-methods

    __abstract__ = True

    def as_dict(self):
        """Serialize a model as a dictionary."""
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
            if isinstance(d[column.name], Decimal):
                d[column.name] = int(d[column.name])
        return d
