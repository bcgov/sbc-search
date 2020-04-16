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
"""This model manages a CorpState entity."""

from search_api.models.base import BaseModel, db


class CorpState(BaseModel):
    """CorpState entity. Corresponds to the 'corp_state' table.

    corp_num          VARCHAR2    10    4137221
    start_event_id    NUMBER      22    4137221
    end_event_id      NUMBER      22    1930459
    state_typ_cd      CHAR        3     4137221
    dd_corp_num       VARCHAR2    10    11443
    """

    __tablename__ = 'corp_state'

    corp_num = db.Column(db.String(10), primary_key=True)
    start_event_id = db.Column(db.Integer)
    end_event_id = db.Column(db.Integer)
    state_typ_cd = db.Column(db.String(3))
    dd_corp_num = db.Column(db.String(10))

    @staticmethod
    def get_corp_states_by_corp_id(corp_id):
        """Get CorpState by corp_num."""
        return CorpState.query.filter(
            CorpState.corp_num == corp_id,
            CorpState.end_event_id == None).all()  # noqa: E711 # pylint: disable=singleton-comparison
