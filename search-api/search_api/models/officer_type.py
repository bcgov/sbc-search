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
'''This model manages a OfficerType entity.'''

from search_api.models.base import BaseModel, db


class OfficerType(BaseModel):
    '''OfficerType entity. Corresponds to the 'officer_type' table.

    officer_typ_cd    CHAR        3      9
    short_desc        VARCHAR2    75     9
    full_desc         VARCHAR2    125    9
    '''

    # pylint: disable=too-few-public-methods

    __tablename__ = 'officer_type'

    officer_typ_cd = db.Column(db.String(3), primary_key=True)
    short_desc = db.Column(db.String(75))
    full_desc = db.Column(db.String(125))
