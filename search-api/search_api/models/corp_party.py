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
"""This model manages a CorpParty entity."""

from functools import reduce
import logging

from sqlalchemy import func, and_, case
from sqlalchemy.orm import aliased
from sqlalchemy.orm.exc import NoResultFound

from search_api.constants import ADDITIONAL_COLS_ACTIVE, ADDITIONAL_COLS_ADDRESS
from search_api.models.base import BaseModel, db
from search_api.models.corp_name import CorpName
from search_api.models.corp_state import CorpState
from search_api.models.corp_op_state import CorpOpState
from search_api.models.address import Address
from search_api.models.event import Event
from search_api.models.filing import Filing
from search_api.models.filing_type import FilingType
from search_api.models.offices_held import OfficesHeld
from search_api.models.officer_type import OfficerType
from search_api.models.party_type import PartyType
from search_api.utils.model_utils import (
    _get_filter,
    _sort_by_field,
    _is_addr_search,
    _merge_addr_fields,
)


logger = logging.getLogger(__name__)


class CorpParty(BaseModel):
    """CorpParty entity. Corresponds to the 'corp_party' table.

    corp_party_id             NUMBER      22     11748880
    mailing_addr_id           NUMBER      22     8369745
    delivery_addr_id          NUMBER      22     7636885
    corp_num                  VARCHAR2    10     11748884
    party_typ_cd              CHAR        3      11748884
    start_event_id            NUMBER      22     11748884
    end_event_id              NUMBER      22     6194691
    prev_party_id             NUMBER      22     3623071
    corr_typ_cd               CHAR        1      230615
    last_report_dt            DATE        7      50
    appointment_dt            DATE        7      3394297
    cessation_dt              DATE        7      3071988
    last_nme                  VARCHAR2    30     11397162
    middle_nme                VARCHAR2    30     2773092
    first_nme                 VARCHAR2    30     11392744
    business_nme              VARCHAR2    150    369824
    bus_company_num           VARCHAR2    15     108582
    email_address             VARCHAR2    254    10442
    corp_party_seq_num        NUMBER      22     27133
    OFFICE_NOTIFICATION_DT    DATE        7      8380
    phone                     VARCHAR2    30     4306
    reason_typ_cd             VARCHAR2    3      0
    """

    __tablename__ = 'corp_party'

    corp_party_id = db.Column(db.Integer, primary_key=True)
    mailing_addr_id = db.Column(db.Integer)
    delivery_addr_id = db.Column(db.Integer)
    corp_num = db.Column(db.String(10))
    party_typ_cd = db.Column(db.String(3))
    start_event_id = db.Column(db.Integer)
    end_event_id = db.Column(db.Integer)
    prev_party_id = db.Column(db.Integer)
    corr_typ_cd = db.Column(db.String(1))
    last_report_dt = db.Column(db.Date)
    appointment_dt = db.Column(db.Date)
    cessation_dt = db.Column(db.Date)
    last_nme = db.Column(db.String(30))
    middle_nme = db.Column(db.String(30))
    first_nme = db.Column(db.String(30))
    business_nme = db.Column(db.String(150))
    bus_company_num = db.Column(db.String(15))
    email_address = db.Column(db.String(254))
    corp_party_seq_num = db.Column(db.Integer)
    phone = db.Column(db.String(30))
    reason_typ_cd = db.Column(db.String(3))

    def __repr__(self):
        """Return string representation of a CorpParty entity."""
        return 'corp num: {}'.format(self.corp_party_id)

    @staticmethod
    def get_corp_party_by_id(corp_party_id):
        """Get a CorpParty entity by id."""
        corp_party = CorpParty.query.filter(CorpParty.corp_party_id == int(corp_party_id))
        try:
            return corp_party.one()
        except NoResultFound:
            return None

    @staticmethod
    def get_corporation_info_by_corp_party_id(corp_party_id):
        """Get Corporation info by CorpParty id."""
        # local import to prevent circular import
        from search_api.models.corporation import Corporation  # pylint: disable=import-outside-toplevel, cyclic-import

        query = (
            CorpParty.query.filter(CorpParty.corp_party_id == int(corp_party_id))
            .join(Corporation, Corporation.corp_num == CorpParty.corp_num)
            .add_columns(Corporation.corp_typ_cd, Corporation.admin_email)
        )

        try:
            return query.one()
        except NoResultFound:
            return None

    @staticmethod
    def get_filing_description_by_corp_party_id(corp_party_id):
        """Get FilingType info by CorpParty id."""
        return (
            CorpParty.query.join(Event, Event.event_id == CorpParty.start_event_id)
            .join(Filing, Filing.event_id == Event.event_id)
            .join(FilingType, FilingType.filing_typ_cd == Filing.filing_typ_cd)
            .add_columns(FilingType.full_desc)
            .filter(CorpParty.corp_party_id == int(corp_party_id))
            .all()
        )

    @staticmethod
    def get_offices_held_by_corp_party_id(corp_party_id):
        """Get OfficesHeld info by CorpParty id."""
        return (
            CorpParty.query.join(OfficesHeld, OfficesHeld.corp_party_id == CorpParty.corp_party_id)
            .join(OfficerType, OfficerType.officer_typ_cd == OfficesHeld.officer_typ_cd)
            .join(Event, Event.event_id == CorpParty.start_event_id)
            .add_columns(
                CorpParty.corp_party_id,
                OfficerType.officer_typ_cd,
                OfficerType.short_desc,
                CorpParty.appointment_dt,
                Event.event_timestmp,
            )
            .filter(CorpParty.corp_party_id == int(corp_party_id))
            .all()
        )

    @staticmethod
    def get_corp_party_at_same_addr(corp_party_id):
        """Get CorpParty entities at the same mailing or delivery address."""
        person = CorpParty.get_corp_party_by_id(corp_party_id)

        if not person:
            return None

        # one or both addr may be null, handle each case.
        if person.delivery_addr_id or person.mailing_addr_id:
            if person.delivery_addr_id and person.mailing_addr_id:
                expr = (CorpParty.delivery_addr_id == person.delivery_addr_id) | (
                    CorpParty.mailing_addr_id == person.mailing_addr_id
                )
            elif person.delivery_addr_id:
                expr = CorpParty.delivery_addr_id == person.delivery_addr_id
            elif person.mailing_addr_id:
                expr = CorpParty.mailing_addr_id == person.mailing_addr_id

            same_addr = (
                CorpParty.query.join(Event, Event.event_id == CorpParty.start_event_id)
                .add_columns(Event.event_timestmp)
                .filter(expr)
            )
        else:
            same_addr = []

        return same_addr

    @staticmethod
    def get_corp_party_same_name_at_same_addr(corp_party_id):
        """Get CorpParty entities with the same CorpParty name and delivery or mailing address."""
        person = CorpParty.get_corp_party_by_id(corp_party_id)

        if not person:
            return None

        same_name_and_company = CorpParty.query.join(Event, Event.event_id == CorpParty.start_event_id).add_columns(
            Event.event_timestmp
        )

        if person.first_nme:
            same_name_and_company = same_name_and_company.filter(CorpParty.first_nme.ilike(person.first_nme))

        if person.last_nme:
            same_name_and_company = same_name_and_company.filter(CorpParty.last_nme.ilike(person.last_nme))

        if person.corp_num:
            same_name_and_company = same_name_and_company.filter(CorpParty.corp_num.ilike(person.corp_num))

        return same_name_and_company

    @staticmethod
    def search_corp_parties(args):
        """Search for CorpParty entities.

        Querystring parameters as follows:

        You may provide any number of querystring triples such as

        field=ANY_NME|first_nme|last_nme|<any column name>
        &operator=exact|contains|startswith|endswith
        &value=<string>
        &sort_type=asc|desc
        &sort_value=ANY_NME|first_nme|last_nme|<any column name>
        &additional_cols=address|active|none

        For example, to get everyone who has any name that starts with 'Sky', or last name must be exactly 'Little', do:
        curl "http://localhost/api/v1/directors/?field=ANY_NME&operator=startswith&value=Sky&field=last_nme&operator=exact&value=Little&mode=ALL"  # noqa
        """
        fields = args.getlist('field')
        operators = args.getlist('operator')
        values = args.getlist('value')

        # Only triples of clauses are allowed. So, the same number of fields, ops and values.
        if len(fields) != len(operators) or len(operators) != len(values):
            raise Exception(
                'mismatched query param lengths: fields:{} operators:{} values:{}'.format(
                    len(fields), len(operators), len(values)
                )
            )

        results = CorpParty.query_corp_parties(args)

        return results

    @staticmethod
    def query_corp_parties(args):
        """Construct db query for CorpParty search."""
        # local import to prevent circular import
        from search_api.models.corporation import Corporation  # pylint: disable=import-outside-toplevel, cyclic-import

        fields = args.getlist('field')
        operators = args.getlist('operator')
        values = args.getlist('value')
        mode = args.get('mode')
        sort_type = args.get('sort_type')
        sort_value = args.get('sort_value')
        additional_cols = args.get('additional_cols')

        # Zip the lists, so ('last_nme', 'first_nme') , ('contains', 'exact'), ('Sky', 'Apple') =>
        #  (('last_nme', 'contains', 'Sky'), ('first_nme', 'exact', 'Apple'))
        clauses = list(zip(fields, operators, values))

        eventA = aliased(Event)
        eventB = aliased(Event)

        results = (
            CorpParty.query.join(Corporation, Corporation.corp_num == CorpParty.corp_num)
            .join(
                PartyType,
                and_(
                    PartyType.party_typ_cd == CorpParty.party_typ_cd
                ),
            )
            .join(
                CorpState,
                and_(
                    CorpState.corp_num == CorpParty.corp_num,
                    CorpState.end_event_id == None,  # pylint: disable=singleton-comparison
                ),
            )
            .outerjoin(
                CorpName,
                and_(
                    CorpName.end_event_id == None,  # pylint: disable=singleton-comparison
                    # CorpName should be "Corporation" or "Number BC Company"
                    CorpName.corp_name_typ_cd.in_(('CO', 'NB')),
                    Corporation.corp_num == CorpName.corp_num,
                ),
            )
            .outerjoin(
                Address,
                and_(
                    Address.addr_id == CorpParty.mailing_addr_id
                ),
                full=True
            )
            .join(
                eventA,
                and_(
                    eventA.event_id == CorpParty.start_event_id
                ),
            )
            .outerjoin(
                eventB,
                and_(
                    eventB.event_id == CorpParty.end_event_id
                ),
                full=True
            )
            .outerjoin(OfficesHeld, OfficesHeld.corp_party_id == CorpParty.corp_party_id)
            .outerjoin(OfficerType, OfficerType.officer_typ_cd == OfficesHeld.officer_typ_cd)
            .with_entities(
                CorpParty.corp_party_id,
                CorpParty.first_nme,
                CorpParty.middle_nme,
                CorpParty.last_nme,
                eventA.event_timestmp.label('appointment_dt'),
                eventB.event_timestmp.label('cessation_dt'),
                CorpParty.corp_num,
                (PartyType.short_desc + " " + OfficerType.short_desc).label('party_typ_cd'),
                CorpName.corp_nme,
                Corporation.admin_email.label('corp_admin_email'),
            )
        )

        results = CorpParty.add_additional_cols_to_search_query(additional_cols, fields, results)

        # Determine if we will combine clauses with OR or AND. mode=ALL means we use AND. Default mode is OR
        if mode == 'ALL':

            def filter_reducer(accumulator, filter_value):
                return accumulator & _get_filter(*filter_value)

        else:

            def filter_reducer(accumulator, filter_value):
                return accumulator | _get_filter(*filter_value)

        # We use reduce here to join all the items in clauses with the & operator or the | operator.
        # Similar to if we did "|".join(clause), but calling the boolean operator instead.

        filter_grp = reduce(filter_reducer, clauses[1:], _get_filter(*clauses[0]))

        results = results.filter(filter_grp)

        # Sorting
        if sort_type is None:
            results = results.order_by(func.upper(CorpParty.last_nme), CorpParty.corp_num)
        else:
            sort_field = _sort_by_field(sort_type, sort_value)
            results = results.order_by(sort_field)
        return results

    @staticmethod
    def add_additional_cols_to_search_query(additional_cols, fields, query):
        """Add Address or CorpOpState columns to query based on the additional columns toggle."""
        if _is_addr_search(fields) or additional_cols == ADDITIONAL_COLS_ADDRESS:
            query = query.outerjoin(Address, CorpParty.mailing_addr_id == Address.addr_id)
            query = query.add_columns(Address.addr_line_1, Address.addr_line_2, Address.addr_line_3,
                                      Address.city, Address.postal_cd, Address.address_desc)

        if additional_cols == ADDITIONAL_COLS_ACTIVE:
            state_type_case_stmt = case([(CorpOpState.state_typ_cd == 'ACT', 'ACTIVE'), ],
                                        else_='HISTORICAL').label("state_typ_cd")

            query = query.join(CorpOpState, CorpOpState.state_typ_cd == CorpState.state_typ_cd)
            query = query.add_columns(state_type_case_stmt)

        return query

    @staticmethod
    def add_additional_cols_to_search_results(additional_cols, fields, row):
        """Add Address or CorpOpState columns to search results based on the additional columns toggle."""
        additional_result_columns = {}
        if _is_addr_search(fields) or additional_cols == ADDITIONAL_COLS_ADDRESS:
            additional_result_columns['addr'] = _merge_addr_fields(row)
            additional_result_columns['postalCd'] = row.postal_cd

        if additional_cols == ADDITIONAL_COLS_ACTIVE:
            additional_result_columns['stateTypCd'] = row.state_typ_cd

        return additional_result_columns
