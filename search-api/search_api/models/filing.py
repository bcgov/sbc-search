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
'''This model manages a Filing entity.'''

from search_api.models.base import BaseModel, db


class Filing(BaseModel):  # pylint: disable=too-few-public-methods
    '''
    Filing entity. Corresponds to the 'filing' table.

    EVENT_ID            NUMBER      22      13775802
    FILING_TYP_CD       CHAR        5       13775803
    EFFECTIVE_DT        DATE        7       13775801
    CHANGE_DT           DATE        7       386466
    REGISTRATION_DT     DATE        7       0
    PERIOD_END_DT       DATE        7       5529986
    ACCESSION_NUM       CHAR        10      0
    ARRANGEMENT_IND     CHAR        1       8212197
    AUTH_SIGN_DT        DATE        7       8276
    WITHDRAWN_EVENT_ID  NUMBER      22      325
    ODS_TYP_CD          CHAR        2       13119449
    DD_EVENT_ID         NUMBER      22      670145
    ACCESS_CD           VARCHAR2    9       4664766
    NR_NUM              VARCHAR2    10      968307
    COURT_APPR_IND      CHAR        1       15787
    COURT_ORDER_NUM     VARCHAR2    255     2069
    AGM_DATE            DATE        7       582818
    NEW_CORP_NUM        VARCHAR2    10      5
    '''

    __tablename__ = 'filing'

    event_id = db.Column(db.Integer, primary_key=True)
    filing_typ_cd = db.Column(db.String(5))
    effective_dt = db.Column(db.Date)
    change_dt = db.Column(db.Date)
    registration_dt = db.Column(db.Date)
    period_end_dt = db.Column(db.Date)
    accession_num = db.Column(db.String(10))
    arrangement_ind = db.Column(db.String(1))
    auth_sign_dt = db.Column(db.Date)
    withdrawn_event_id = db.Column(db.Integer)
    ods_typ_cd = db.Column(db.String(2))
    dd_event_id = db.Column(db.Integer)
    access_cd = db.Column(db.String(9))
    nr_num = db.Column(db.String(10))
    court_appr_ind = db.Column(db.String(1))
    court_order_num = db.Column(db.String(255))
    agm_date = db.Column(db.Date)
    new_corp_num = db.Column(db.String(10))
