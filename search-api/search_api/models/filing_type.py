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
"""This model manages a FilingType entity."""

from search_api.models.base import BaseModel, db


class FilingType(BaseModel):
    """FilingType entity. Corresponds to the 'filing_type' table.

    FILING_TYP_CD       CHAR        5      420
    FILING_TYP_CLASS    VARCHAR2    10     420
    SHORT_DESC          VARCHAR2    50     420
    FULL_DESC           VARCHAR2    125    420
    """

    # pylint: disable=too-few-public-methods

    __tablename__ = 'filing_type'

    filing_typ_cd = db.Column(db.String(5), primary_key=True)
    filing_typ_class = db.Column(db.String(10))
    short_desc = db.Column(db.String(50))
    full_desc = db.Column(db.String(125))
