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
'''Table of related NickNames. Any name with equivalent name_id is considered related.'''

from sqlalchemy import func
from search_api.models.base import BaseModel, db


class NickName(BaseModel):
    '''NickName table. Note: this table has no pkey.'''

    __tablename__ = 'nickname'

    name_id = db.Column(db.Integer)
    name = db.Column(db.String(30), primary_key=True)

    @staticmethod
    def get_nickname_search_expr(field, value):
        '''Generate an expression to return instances where a field matches any nickname related to the provided value'''
        aliases = db.session.query(NickName.name).filter(
            NickName.name_id
            == db.session.query(NickName.name_id).filter(NickName.name == value)
        )

        alias_list = list(a[0] for a in aliases)
        return func.upper(field).in_(alias_list)
