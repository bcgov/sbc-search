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


class Office(BaseModel):
    __tablename__ = "office"
    """
    corp_num            VARCHAR2    10    4544141
    office_typ_cd       CHAR        2     4544141
    start_event_id      NUMBER      22    4544141
    end_event_id        NUMBER      22    1578071
    mailing_addr_id     NUMBER      22    4533953
    delivery_addr_id    NUMBER      22    4527193
    dd_corp_num         VARCHAR2    10    23155
    email_address       VARCHAR2    75    14906
    """

    corp_num = db.Column(db.String(10), primary_key=True)
    office_typ_cd = db.Column(db.String(2), primary_key=True)
    start_event_id = db.Column(db.Integer, primary_key=True)
    end_event_id = db.Column(db.Integer)
    mailing_addr_id = db.Column(db.Integer)
    delivery_addr_id = db.Column(db.Integer)
    dd_corp_num = db.Column(db.String(10))
    email_address = db.Column(db.String(75))

    @staticmethod
    def get_offices_by_corp_id(id):
        return Office.query.filter_by(corp_num=id, end_event_id=None)
