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
"""This model manages an Event entity."""

from search_api.models.base import BaseModel, db


class Event(BaseModel):
    """Event entity. Corresponds to the 'event' table.

    EVENT_ID          NUMBER      22    17616460
    CORP_NUM          VARCHAR2    10    17616460
    EVENT_TYP_CD      VARCHAR2    10    17616460
    EVENT_TIMESTMP    DATE        7     17616461
    TRIGGER_DTS       DATE        7     1126833
    """

    # pylint: disable=too-few-public-methods

    __tablename__ = 'event'

    event_id = db.Column(db.Integer, unique=True, primary_key=True)
    corp_num = db.Column(db.String(10))
    event_type_cd = db.Column(db.String(10))
    event_timestmp = db.Column(db.Date)
    trigger_dts = db.Column(db.Date)
