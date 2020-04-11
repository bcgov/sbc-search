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
"""This model manages a CorpOpState entity."""

from search_api.models.base import BaseModel, db


class CorpOpState(BaseModel):
    """
    A lookup table of states a corporation can be in.

    state_typ_cd       CHAR        3     31
    op_state_typ_cd    CHAR        3     31
    short_desc         VARCHAR2    15    31
    full_desc          VARCHAR2    40    31
    """

    # pylint: disable=too-few-public-methods

    __tablename__ = 'corp_op_state'

    state_typ_cd = db.Column(db.String(3), primary_key=True)
    op_state_typ_cd = db.Column(db.String(3))
    short_desc = db.Column(db.String(15))
    full_desc = db.Column(db.String(40))
