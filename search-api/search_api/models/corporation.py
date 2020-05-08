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
"""This model manages a Corporation entity."""

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_, func
from sqlalchemy.sql.expression import literal_column

from search_api.models.base import BaseModel, db
from search_api.models.corp_name import CorpName
from search_api.models.corp_state import CorpState
from search_api.models.office import Office
from search_api.models.address import Address
from search_api.utils.model_utils import _sort_by_field


class Corporation(BaseModel):
    """Corporation entity. Corresponds to the 'corporation' table.

    corp_num                       VARCHAR2    10     2206759
    corp_frozen_typ_cd             CHAR        1      819
    corp_typ_cd                    VARCHAR2    3      2206759
    recognition_dts                DATE        7      2111082
    last_ar_filed_dt               DATE        7      1025542
    transition_dt                  DATE        7      240802
    bn_9                           VARCHAR2    9      1179842
    bn_15                          VARCHAR2    15     1179165
    accession_num                  VARCHAR2    10     941
    CORP_PASSWORD                  VARCHAR2    300    795500
    PROMPT_QUESTION                VARCHAR2    100    573423
    admin_email                    VARCHAR2    254    703636
    send_ar_ind                    VARCHAR2    1      1642638
    tilma_involved_ind             VARCHAR2    1      2196814
    tilma_cessation_dt             DATE        7      4050
    firm_last_image_date           DATE        7      51550
    os_session                     NUMBER      22     420543
    last_agm_date                  DATE        7      48416
    firm_lp_xp_termination_date    DATE        7      7443
    last_ledger_dt                 DATE        7      1
    ar_reminder_option             VARCHAR2    10     69086
    ar_reminder_date               VARCHAR2    20     67640
    TEMP_PASSWORD                  VARCHAR2    300    3582
    TEMP_PASSWORD_EXPIRY_DATE      DATE        7      3582
    """

    __tablename__ = 'corporation'

    corp_num = db.Column(db.String(10), primary_key=True, unique=True)
    corp_frozen_typ_cd = db.Column(db.String(1))
    corp_typ_cd = db.Column(db.String(3))
    recognition_dts = db.Column(db.Date)
    last_ar_filed_dt = db.Column(db.Date)
    transition_dt = db.Column(db.Date)
    bn_9 = db.Column(db.String(9))
    bn_15 = db.Column(db.String(15))
    accession_num = db.Column(db.String(10))
    admin_email = db.Column(db.String(254))
    send_ar_ind = db.Column(db.String(1))
    tilma_involved_ind = db.Column(db.String(1))
    tilma_cessation_dt = db.Column(db.Date)
    firm_last_image_date = db.Column(db.Date)
    os_session = db.Column(db.Integer)
    last_agm_date = db.Column(db.Date)
    firm_lp_xp_termination_date = db.Column(db.Date)
    last_ledger_dt = db.Column(db.Date)
    ar_reminder_option = db.Column(db.String(10))
    ar_reminder_date = db.Column(db.String(20))

    def __repr__(self):
        """Return string representation of a Corporation entity."""
        return 'corp num: {}'.format(self.corp_num)

    @staticmethod
    def get_corporation_by_id(corp_id):
        """Get a corporation by id."""
        query = Corporation.query.add_columns(
            Corporation.corp_num, Corporation.transition_dt, Corporation.admin_email
        ).filter(Corporation.corp_num == corp_id)

        try:
            return query.one()
        except NoResultFound:
            return None

    @staticmethod
    def search_corporations(args, include_addr=False):
        """Search for Corporations by query (search keyword or corpNum) and sort results."""
        query = args.get('query')

        sort_type = args.get('sort_type')
        sort_value = args.get('sort_value')
        search_field = args.get('search_field', 'corpNme')

        results = Corporation.query_corporations(query, search_field, sort_type, sort_value, include_addr)
        return results

    @staticmethod
    def query_corporations(query, search_field, sort_type, sort_value, include_addr=False):
        """Construct Corporation search db query."""
        results = (
            Corporation.query.outerjoin(
                CorpName,
                and_(
                    CorpName.end_event_id == None,  # noqa  # pylint: disable=singleton-comparison
                    Corporation.corp_num == CorpName.corp_num,  # noqa
                    CorpName.corp_name_typ_cd.in_(('CO', 'NB')),  # noqa
                ),
            )
            .outerjoin(
                CorpState,
                and_(
                    CorpState.corp_num == Corporation.corp_num,  # noqa
                    CorpState.state_typ_cd == 'ACT',  # noqa
                    CorpState.end_event_id == None,  # noqa  # pylint: disable=singleton-comparison
                ),
            )
            .outerjoin(
                Office,
                and_(
                    Office.corp_num == Corporation.corp_num,  # noqa
                    Office.office_typ_cd != literal_column("'RG'"),  # noqa
                    Office.end_event_id == None,  # noqa  # pylint: disable=singleton-comparison
                ),
            )
            .outerjoin(Address, Office.mailing_addr_id == Address.addr_id)
        )

        if include_addr:
            results = results.with_entities(
                CorpName.corp_nme,
                Corporation.corp_num,
                Corporation.corp_typ_cd,
                Corporation.recognition_dts,
                CorpState.state_typ_cd,
                Address.addr_line_1,
                Address.addr_line_2,
                Address.addr_line_3,
                Address.city,
                Address.postal_cd,
            )
        else:
            results = results.with_entities(
                CorpName.corp_nme,
                Corporation.corp_num,
                Corporation.corp_typ_cd,
                Corporation.recognition_dts,
                CorpState.state_typ_cd,
            )

        if search_field == 'corpNme':
            results = results.filter(
                # or_(
                # TODO: This OR query leads to poor performance. We may need a UI control to
                # choose which field to search.
                # For now, we only support company names.
                #    Corporation.corp_num == query.upper(),
                CorpName.corp_name_typ_cd == literal_column("'CO'"),
                # Doing a full CONTAINS search is quite slow. Use STARTSWITH for this reason.
                func.upper(CorpName.corp_nme).like('%' + query.upper() + '%')
                # )
            )
        elif search_field == 'corpNum':
            results = results.filter(Corporation.corp_num == query.upper(),)
        else:
            raise Exception('Invalid search field specified: `{}`'.format(search_field))

        # Sorting
        if sort_type is None:
            # Note: The Oracle back-end performs better with UPPER() compared to LOWER() case casting.
            results = results.order_by(func.upper(CorpName.corp_nme))
        else:
            sort_field_str = _sort_by_field(sort_type, sort_value)

            results = results.order_by(sort_field_str)
        return results
