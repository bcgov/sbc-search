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
"""This model manages an PartyType entity."""

from search_api.models.base import BaseModel, db


class PartyType(BaseModel):  # pylint: disable=too-few-public-methods
    """PartyType entity. Corresponds to the 'party_type' table.

    PARTY_TYP_CD                   CHAR                           3                   24
    SHORT_DESC                     VARCHAR2                       75                  24
    FULL_DESC                      VARCHAR2                       250                 24
    """

    __tablename__ = 'party_type'

    party_typ_cd = db.Column(db.String(3), primary_key=True)
    short_desc = db.Column(db.String(75))
    full_desc = db.Column(db.String(250))
