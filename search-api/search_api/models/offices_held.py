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

from search_api.models.base import BaseModel, db


class OfficesHeld(BaseModel):
    __tablename__ = "offices_held"
    """
    corp_party_id       NUMBER    22    3694791
    officer_typ_cd      CHAR      3     3694794
    dd_corp_party_id    NUMBER    22    7
    """

    corp_party_id = db.Column(db.Integer, primary_key=True)
    officer_typ_cd = db.Column(db.String(3), primary_key=True)
    dd_corp_party_id = db.Column(db.Integer)
