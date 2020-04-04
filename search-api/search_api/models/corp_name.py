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

from sqlalchemy import desc

from search_api.models.base import BaseModel, db


class CorpName(BaseModel):
    __tablename__ = 'corp_name'
    """
    corp_num             VARCHAR2    10     2484908
    corp_name_typ_cd     CHAR        2      2484908
    start_event_id       NUMBER      22     2484908
    corp_name_seq_num    NUMBER      22     2484908
    end_event_id         NUMBER      22     251437
    srch_nme             VARCHAR2    35     2484908
    corp_nme             VARCHAR2    150    2484909
    dd_corp_num          VARCHAR2    10     11929
    """

    corp_num = db.Column(db.String(10), primary_key=True)
    corp_name_seq_num = db.Column(db.Integer)
    corp_name_typ_cd = db.Column(db.String(2))
    start_event_id = db.Column(db.Integer)
    end_event_id = db.Column(db.Integer)
    srch_nme = db.Column(db.String(35))
    corp_nme = db.Column(db.String(150))
    dd_corp_num = db.Column(db.String(10))

    def __repr__(self):
        return 'corp num: {}'.format(self.corp_num)

    @staticmethod
    def get_corp_name_by_corp_id(id):
        return CorpName.query.filter_by(corp_num=id).order_by(desc(CorpName.end_event_id))
