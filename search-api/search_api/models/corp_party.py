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

from functools import reduce

from sqlalchemy import func

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
from search_api.utils.model_utils import _get_filter, _sort_by_field


class CorpParty(BaseModel):
    __tablename__ = 'corp_party'

    """
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
        return 'corp num: {}'.format(self.corp_party_id)

    @staticmethod
    def get_corp_party_by_id(id):
        return CorpParty.query.filter(CorpParty.corp_party_id == int(id)).one()

    @staticmethod
    def get_corporation_info_by_corp_party_id(id):
        # local import to prevent circular import
        from search_api.models.corporation import Corporation

        return (
            CorpParty.query.filter(CorpParty.corp_party_id == int(id))
            .join(Corporation, Corporation.corp_num == CorpParty.corp_num)
            .add_columns(
                Corporation.corp_typ_cd,
                Corporation.admin_email
            ).one())

    @staticmethod
    def get_filing_description_by_corp_party_id(id):
        return (
            CorpParty.query
            .join(Event, Event.event_id == CorpParty.start_event_id)
            .join(Filing, Filing.event_id == Event.event_id)
            .join(FilingType, FilingType.filing_typ_cd == Filing.filing_typ_cd)
            .add_columns(FilingType.full_desc)
            .filter(CorpParty.corp_party_id == int(id)).all())

    @staticmethod
    def get_offices_held_by_corp_party_id(id):
        return (
            CorpParty.query
            .join(OfficesHeld, OfficesHeld.corp_party_id == CorpParty.corp_party_id)
            .join(OfficerType, OfficerType.officer_typ_cd == OfficesHeld.officer_typ_cd)
            .join(Event, Event.event_id == CorpParty.start_event_id)
            .add_columns(
                CorpParty.corp_party_id,
                OfficerType.officer_typ_cd,
                OfficerType.short_desc,
                CorpParty.appointment_dt,
                Event.event_timestmp
            )
            .filter(CorpParty.corp_party_id == int(id))
        )

    @staticmethod
    def get_corp_party_at_same_addr(id):
        person = CorpParty.get_corp_party_by_id(id)

        # one or both addr may be null, handle each case.
        if person.delivery_addr_id or person.mailing_addr_id:
            if person.delivery_addr_id and person.mailing_addr_id:
                expr = (CorpParty.delivery_addr_id == person.delivery_addr_id) | \
                    (CorpParty.mailing_addr_id == person.mailing_addr_id)
            elif person.delivery_addr_id:
                expr = (CorpParty.delivery_addr_id == person.delivery_addr_id)
            elif person.mailing_addr_id:
                expr = (CorpParty.mailing_addr_id == person.mailing_addr_id)

            same_addr = (
                CorpParty.query
                .join(Event, Event.event_id == CorpParty.start_event_id)
                .add_columns(Event.event_timestmp)
                .filter(expr)
            )
        else:
            same_addr = []

        return same_addr

    @staticmethod
    def get_corp_party_same_name_at_same_addr(id):
        person = CorpParty.get_corp_party_by_id(id)
        same_name_and_company = (
            CorpParty.query
            .join(Event, Event.event_id == CorpParty.start_event_id)
            .add_columns(Event.event_timestmp)
        )

        if person.first_nme:
            same_name_and_company = same_name_and_company.filter(
                CorpParty.first_nme.ilike(person.first_nme))

        if person.last_nme:
            same_name_and_company = same_name_and_company.filter(
                CorpParty.last_nme.ilike(person.last_nme))

        if person.corp_num:
            same_name_and_company = same_name_and_company.filter(
                CorpParty.corp_num.ilike(person.corp_num))

        return same_name_and_company

    @staticmethod
    def search_corp_parties(args):
        """
        Querystring parameters as follows:

        You may provide any number of querystring triples such as

        field=ANY_NME|first_nme|last_nme|<any column name>
        &operator=exact|contains|startswith|endswith
        &value=<string>
        &sort_type=asc|desc
        &sort_value=ANY_NME|first_nme|last_nme|<any column name>

        For example, to get everyone who has any name that starts with 'Sky', or last name must be exactly 'Little', do:
        curl "http://localhost/api/v1/directors/?field=ANY_NME&operator=startswith&value=Sky&field=last_nme&operator=exact&value=Little&mode=ALL"  # noqa
        """

        query = args.get("query")

        fields = args.getlist('field')
        operators = args.getlist('operator')
        values = args.getlist('value')
        mode = args.get('mode')
        sort_type = args.get('sort_type')
        sort_value = args.get('sort_value')

        if query and len(fields) > 0:
            raise Exception("use simple query or advanced. don't mix")

        # Only triples of clauses are allowed. So, the same number of fields, ops and values.
        if len(fields) != len(operators) or len(operators) != len(values):
            raise Exception("mismatched query param lengths: fields:{} operators:{} values:{}".format(
                len(fields),
                len(operators),
                len(values)))

        # Zip the lists, so ('last_nme', 'first_nme') , ('contains', 'exact'), ('Sky', 'Apple') =>
        #  (('last_nme', 'contains', 'Sky'), ('first_nme', 'exact', 'Apple'))
        clauses = list(zip(fields, operators, values))

        results = CorpParty.query_corp_parties(clauses, mode, sort_type, sort_value)

        return results

    @staticmethod
    def query_corp_parties(clauses, mode, sort_type, sort_value):
        # local import to prevent circular import
        from search_api.models.corporation import Corporation

        results = (
            CorpParty.query
            .join(Corporation, Corporation.corp_num == CorpParty.corp_num)
            .join(CorpState, CorpState.corp_num == CorpParty.corp_num)
            .join(CorpOpState, CorpOpState.state_typ_cd == CorpState.state_typ_cd)
            .outerjoin(CorpName, Corporation.corp_num == CorpName.corp_num)
            .outerjoin(Address, CorpParty.mailing_addr_id == Address.addr_id)
            .add_columns(
                CorpParty.corp_party_id,
                CorpParty.first_nme,
                CorpParty.middle_nme,
                CorpParty.last_nme,
                CorpParty.appointment_dt,
                CorpParty.cessation_dt,
                CorpParty.corp_num,
                CorpParty.party_typ_cd,
                CorpName.corp_nme,
                Address.addr_line_1,
                Address.addr_line_2,
                Address.addr_line_3,
                Address.postal_cd,
                CorpOpState.state_typ_cd,
            )).filter(
                CorpParty.end_event_id == None,  # noqa
                CorpState.end_event_id == None,
                CorpName.end_event_id == None,
                # CorpName should be "Corporation" or "Number BC Company"
                CorpName.corp_name_typ_cd.in_(("CO", "NB"))
            )

        # Determine if we will combine clauses with OR or AND. mode=ALL means we use AND. Default mode is OR
        if mode == 'ALL':
            def fn(accumulator, s):
                return accumulator & _get_filter(*s)
        else:
            def fn(accumulator, s):
                return accumulator | _get_filter(*s)

        # We use reduce here to join all the items in clauses with the & operator or the | operator.
        # Similar to if we did "|".join(clause), but calling the boolean operator instead.
        filter_grp = reduce(
            fn,
            clauses[1:],
            _get_filter(*clauses[0])
        )
        results = results.filter(filter_grp)

        # Sorting
        if sort_type is None:
            results = results.order_by(func.lower(CorpParty.last_nme), CorpParty.corp_num)
        else:
            sort_field_str = _sort_by_field(sort_type, sort_value)
            results = results.order_by(eval(sort_field_str))

        return results
