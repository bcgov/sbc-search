from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import os
from decimal import Decimal
import decimal
import flask.json
from search_api.constants import ADDITIONAL_COLS_ADDRESS, ADDITIONAL_COLS_ACTIVE
from functools import reduce

class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)

flask.json_encoder = MyJSONEncoder

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_URL', 'postgresql://postgres:password@db/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class BaseModel(db.Model):
    __abstract__ = True
    #__table_args__ = {'quote':False, 'schema': 'bc_registries'}
    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = getattr(self, c.name)
            if type(d[c.name]) is Decimal:
                d[c.name] = int(d[c.name])
        return d


class Address(BaseModel):
    __tablename__ = "address"
    """
    Original Schema from Oracle DB
    ADDRESS                        addr_id                        NUMBER                         22                             20233825
    ADDRESS                        province                       CHAR                           2                              18872463
    ADDRESS                        country_typ_cd                 CHAR                           2                              19016927
    ADDRESS                        postal_cd                      VARCHAR2                       15                             18825296
    ADDRESS                        addr_line_1                    VARCHAR2                       50                             16862093
    ADDRESS                        addr_line_2                    VARCHAR2                       50                             3609613
    ADDRESS                        addr_line_3                    VARCHAR2                       50                             482762
    ADDRESS                        city                           VARCHAR2                       40                             17557057
    ADDRESS                        address_format_type            VARCHAR2                       10                             3632701
    ADDRESS                        address_desc                   VARCHAR2                       300                            3372387
    ADDRESS                        address_desc_short             VARCHAR2                       300                            3350206
    ADDRESS                        delivery_instructions          VARCHAR2                       80                             34510
    ADDRESS                        unit_no                        VARCHAR2                       6                              699964
    ADDRESS                        unit_type                      VARCHAR2                       10                             11488
    ADDRESS                        civic_no                       VARCHAR2                       6                              2210964
    ADDRESS                        civic_no_suffix                VARCHAR2                       10                             15768
    ADDRESS                        street_name                    VARCHAR2                       30                             2221177
    ADDRESS                        street_type                    VARCHAR2                       10                             2167805
    ADDRESS                        street_direction               VARCHAR2                       10                             292073
    ADDRESS                        lock_box_no                    VARCHAR2                       5                              115988
    ADDRESS                        installation_type              VARCHAR2                       10                             47289
    ADDRESS                        installation_name              VARCHAR2                       30                             47036
    ADDRESS                        installation_qualifier         VARCHAR2                       15                             69
    ADDRESS                        route_service_type             VARCHAR2                       10                             146477
    ADDRESS                        route_service_no               VARCHAR2                       4                              27530
    ADDRESS                        province_state_name            VARCHAR2                       30                             362
    """

    addr_id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(2))
    country_typ_cd = db.Column(db.String(2))
    postal_cd = db.Column(db.String(15))
    addr_line_1 = db.Column(db.String(50))
    addr_line_2 = db.Column(db.String(50))
    addr_line_3 = db.Column(db.String(50))
    city = db.Column(db.String(40))
    address_format_type = db.Column(db.String(10))
    address_desc = db.Column(db.String(300))
    address_desc_short = db.Column(db.String(300))
    delivery_instructions = db.Column(db.String(80))
    unit_no = db.Column(db.String(6))
    unit_type = db.Column(db.String(10))
    civic_no = db.Column(db.String(6))
    civic_no_suffix = db.Column(db.String(10))
    street_name = db.Column(db.String(30))
    street_type = db.Column(db.String(10))
    street_direction = db.Column(db.String(10))
    lock_box_no = db.Column(db.String(5))
    installation_type = db.Column(db.String(10))
    installation_name = db.Column(db.String(30))
    installation_qualifier = db.Column(db.String(15))
    route_service_type = db.Column(db.String(10))
    route_service_no = db.Column(db.String(4))
    province_state_name = db.Column(db.String(30))


class CorpOpState(BaseModel):
    # A lookup table of states a corporation can be in.
    __tablename__ = 'corp_op_state'
    """
    CORP_OP_STATE                  state_typ_cd                   CHAR                           3                              31
    CORP_OP_STATE                  op_state_typ_cd                CHAR                           3                              31
    CORP_OP_STATE                  short_desc                     VARCHAR2                       15                             31
    CORP_OP_STATE                  full_desc                      VARCHAR2                       40                             31
    """

    state_typ_cd = db.Column(db.String(3), primary_key=True)
    op_state_typ_cd = db.Column(db.String(3))
    short_desc = db.Column(db.String(15))
    full_desc = db.Column(db.String(40))


class CorpState(BaseModel):
    __tablename__ = 'corp_state'
    """
    CORP_STATE                     corp_num                       VARCHAR2                       10                             4137221
    CORP_STATE                     start_event_id                 NUMBER                         22                             4137221
    CORP_STATE                     end_event_id                   NUMBER                         22                             1930459
    CORP_STATE                     state_typ_cd                   CHAR                           3                              4137221
    CORP_STATE                     dd_corp_num                    VARCHAR2                       10                             11443
    """

    corp_num = db.Column(db.String(10), primary_key=True)
    start_event_id = db.Column(db.Integer)
    end_event_id = db.Column(db.Integer)
    state_typ_cd = db.Column(db.String(3))
    dd_corp_num = db.Column(db.String(10))


class Corporation(BaseModel):
    __tablename__ = 'corporation'
    """
    CORPORATION                    corp_num                       VARCHAR2                       10                             2206759
    CORPORATION                    corp_frozen_typ_cd             CHAR                           1                              819
    CORPORATION                    corp_typ_cd                    VARCHAR2                       3                              2206759
    CORPORATION                    recognition_dts                DATE                           7                              2111082
    CORPORATION                    last_ar_filed_dt               DATE                           7                              1025542
    CORPORATION                    transition_dt                  DATE                           7                              240802
    CORPORATION                    bn_9                           VARCHAR2                       9                              1179842
    CORPORATION                    bn_15                          VARCHAR2                       15                             1179165
    CORPORATION                    accession_num                  VARCHAR2                       10                             941
    CORPORATION                    CORP_PASSWORD                  VARCHAR2                       300                            795500
    CORPORATION                    PROMPT_QUESTION                VARCHAR2                       100                            573423
    CORPORATION                    admin_email                    VARCHAR2                       254                            703636
    CORPORATION                    send_ar_ind                    VARCHAR2                       1                              1642638
    CORPORATION                    tilma_involved_ind             VARCHAR2                       1                              2196814
    CORPORATION                    tilma_cessation_dt             DATE                           7                              4050
    CORPORATION                    firm_last_image_date           DATE                           7                              51550
    CORPORATION                    os_session                     db.Integer                         22                             420543
    CORPORATION                    last_agm_date                  DATE                           7                              48416
    CORPORATION                    firm_lp_xp_termination_date    DATE                           7                              7443
    CORPORATION                    last_ledger_dt                 DATE                           7                              1
    CORPORATION                    ar_reminder_option             VARCHAR2                       10                             69086
    CORPORATION                    ar_reminder_date               VARCHAR2                       20                             67640
    CORPORATION                    TEMP_PASSWORD                  VARCHAR2                       300                            3582
    CORPORATION                    TEMP_PASSWORD_EXPIRY_DATE      DATE                           7                              3582
    """

    corp_num = db.Column(db.String(10), primary_key=True, unique=True)
    corp_frozen_typ_cd = db.Column(db.String(1))
    corp_typ_cd = db.Column(db.String(3))
    recognition_dts = db.Column(db.Date)
    last_ar_filed_dt = db.Column(db.Date)
    transition_dt = db.Column(db.Date)
    bn_9 = db.Column(db.String(9))
    bn_15 = db.Column(db.String(15))
    accession_num = db.Column(db.String(10))
    # CORP_PASSWORD = db.Column(db.String(300))
    # PROMPT_QUESTION = db.Column(db.String(100))
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
    # TEMP_PASSWORD = db.Column(db.String(300))
    # TEMP_PASSWORD_EXPIRY_DATE = db.Column(db.Date)

    def __repr__(self):
        return 'corp num: {}'.format(self.corp_num)


class CorpName(BaseModel):
    __tablename__ = 'corp_name'
    """
    CORP_NAME                      corp_num                       VARCHAR2                       10                             2484908
    CORP_NAME                      corp_name_typ_cd               CHAR                           2                              2484908
    CORP_NAME                      start_event_id                 NUMBER                         22                             2484908
    CORP_NAME                      corp_name_seq_num              NUMBER                         22                             2484908
    CORP_NAME                      end_event_id                   NUMBER                         22                             251437
    CORP_NAME                      srch_nme                       VARCHAR2                       35                             2484908
    CORP_NAME                      corp_nme                       VARCHAR2                       150                            2484909
    CORP_NAME                      dd_corp_num                    VARCHAR2                       10                             11929
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


class Office(BaseModel):
    __tablename__ = "office"
    """
    OFFICE                         corp_num                       VARCHAR2                       10                             4544141
    OFFICE                         office_typ_cd                  CHAR                           2                              4544141
    OFFICE                         start_event_id                 NUMBER                         22                             4544141
    OFFICE                         end_event_id                   NUMBER                         22                             1578071
    OFFICE                         mailing_addr_id                NUMBER                         22                             4533953
    OFFICE                         delivery_addr_id               NUMBER                         22                             4527193
    OFFICE                         dd_corp_num                    VARCHAR2                       10                             23155
    OFFICE                         email_address                  VARCHAR2                       75                             14906
    """

    corp_num = db.Column(db.String(10), primary_key=True)
    office_typ_cd = db.Column(db.String(2), primary_key=True)
    start_event_id = db.Column(db.Integer, primary_key=True)
    end_event_id = db.Column(db.Integer)
    mailing_addr_id = db.Column(db.Integer)
    delivery_addr_id = db.Column(db.Integer)
    dd_corp_num = db.Column(db.String(10))
    email_address = db.Column(db.String(75))


class OfficeType(BaseModel):
    __tablename__ = "office_type"
    """
    OFFICE_TYPE                    office_typ_cd                  CHAR                           2                              9
    OFFICE_TYPE                    short_desc                     VARCHAR2                       15                             9
    OFFICE_TYPE                    full_desc                      VARCHAR2                       40                             9
    """

    office_typ_cd = db.Column(db.String(2), primary_key=True)
    short_desc = db.Column(db.String(15))
    full_desc = db.Column(db.String(40))


class CorpParty(BaseModel):
    __tablename__ = 'corp_party'

    """
    CORP_PARTY                     corp_party_id                  db.Integer                         22                             11748880
    CORP_PARTY                     mailing_addr_id                db.Integer                         22                             8369745
    CORP_PARTY                     delivery_addr_id               db.Integer                         22                             7636885
    CORP_PARTY                     corp_num                       VARCHAR2                       10                             11748884
    CORP_PARTY                     party_typ_cd                   CHAR                           3                              11748884
    CORP_PARTY                     start_event_id                 db.Integer                         22                             11748884
    CORP_PARTY                     end_event_id                   db.Integer                         22                             6194691
    CORP_PARTY                     prev_party_id                  db.Integer                         22                             3623071
    CORP_PARTY                     corr_typ_cd                    CHAR                           1                              230615
    CORP_PARTY                     last_report_dt                 DATE                           7                              50
    CORP_PARTY                     appointment_dt                 DATE                           7                              3394297
    CORP_PARTY                     cessation_dt                   DATE                           7                              3071988
    CORP_PARTY                     last_nme                       VARCHAR2                       30                             11397162
    CORP_PARTY                     middle_nme                     VARCHAR2                       30                             2773092
    CORP_PARTY                     first_nme                      VARCHAR2                       30                             11392744
    CORP_PARTY                     business_nme                   VARCHAR2                       150                            369824
    CORP_PARTY                     bus_company_num                VARCHAR2                       15                             108582
    CORP_PARTY                     email_address                  VARCHAR2                       254                            10442
    CORP_PARTY                     corp_party_seq_num             db.Integer                         22                             27133
    CORP_PARTY                     OFFICE_NOTIFICATION_DT         DATE                           7                              8380
    CORP_PARTY                     phone                          VARCHAR2                       30                             4306
    CORP_PARTY                     reason_typ_cd                  VARCHAR2                       3                              0
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

class Event(BaseModel):
    __tablename__ = "event"
    """
    EVENT_ID                       NUMBER                         22                             17616460
    CORP_NUM                       VARCHAR2                       10                             17616460
    EVENT_TYP_CD                   VARCHAR2                       10                             17616460
    EVENT_TIMESTMP                 DATE                           7                              17616461
    TRIGGER_DTS                    DATE                           7                              1126833
    """

    event_id = db.Column(db.Integer, unique=True, primary_key=True)
    corp_num = db.Column(db.String(10))
    event_type_cd = db.Column(db.String(10))
    event_timestmp = db.Column(db.Date)
    trigger_dts = db.Column(db.Date)


class OfficerType(BaseModel):
    __tablename__ = "officer_type"
    """
    OFFICER_TYPE                   officer_typ_cd                 CHAR                           3                              9
    OFFICER_TYPE                   short_desc                     VARCHAR2                       75                             9
    OFFICER_TYPE                   full_desc                      VARCHAR2                       125                            9
    """

    officer_typ_cd = db.Column(db.String(3), primary_key=True)
    short_desc = db.Column(db.String(75))
    full_desc = db.Column(db.String(125))


class OfficesHeld(BaseModel):
    __tablename__ = "offices_held"
    """
    OFFICES_HELD                   corp_party_id                  NUMBER                         22                             3694791
    OFFICES_HELD                   officer_typ_cd                 CHAR                           3                              3694794
    OFFICES_HELD                   dd_corp_party_id               NUMBER                         22                             7
    """

    corp_party_id = db.Column(db.Integer, primary_key=True)
    officer_typ_cd = db.Column(db.String(3), primary_key=True)
    dd_corp_party_id = db.Column(db.Integer)



def _merge_corpparty_search_addr_fields(row):
    address = row.addr_line_1
    if row.addr_line_2:
        address += ", " + row.addr_line_2
    if row.addr_line_3:
        address += ", " + row.addr_line_3
    return address


def _is_addr_search(fields):
    return "addr_line_1" in fields or "postal_cd" in fields


def _add_additional_cols_to_search_results(args, row, result_dict):
    fields = args.getlist('field')
    additional_cols = args.get('additional_cols')
    if _is_addr_search(fields) or additional_cols == ADDITIONAL_COLS_ADDRESS:
        result_dict['addr'] = _merge_corpparty_search_addr_fields(row)
        result_dict['postal_cd'] = row.postal_cd
    elif additional_cols == ADDITIONAL_COLS_ACTIVE:
        result_dict['state_typ_cd'] = row.state_typ_cd


def _add_additional_cols_to_search_query(args, query):
    fields = args.getlist('field')
    additional_cols = args.get('additional_cols')
    if _is_addr_search(fields) or additional_cols == ADDITIONAL_COLS_ADDRESS:
        query = query.join(Address, CorpParty.mailing_addr_id == Address.addr_id)
        query = query.add_columns(
            Address.addr_line_1,
            Address.addr_line_2,
            Address.addr_line_3,
            Address.postal_cd)
    elif additional_cols == ADDITIONAL_COLS_ACTIVE:
        query = query.join(CorpState, CorpState.corp_num == CorpParty.corp_num)\
            .join(CorpOpState, CorpOpState.state_typ_cd == CorpState.state_typ_cd)
        query = query.add_columns(CorpOpState.state_typ_cd)

    return query


def _get_model_by_field(field_name):

    # return CorpParty
    # [cvo] for performance we only query this one above table for now.

    if field_name in ['first_nme', 'middle_nme', 'last_nme', 'appointment_dt', 'cessation_dt', 'corp_num',
                      'corp_party_id']:  # CorpParty fields
        return eval('CorpParty')
    # elif field_name in ['corp_num']: # Corporation fields
    #     return eval('Corporation')
    # elif field_name in ['corp_nme']: # CorpName fields
    #     return eval('CorpName')
    elif field_name in ['addr_line_1','addr_line_2','addr_line_3','postal_cd','city','province']: # Address fields
        return eval('Address')

    #return None


def _get_filter(field, operator, value):

    if field == 'any_nme':
        return (_get_filter('first_nme', operator, value)
            | _get_filter('middle_nme', operator, value)
            | _get_filter('last_nme', operator, value))

    if field == 'addr':
        # return _get_filter('first_nme', operator, value)
        return (_get_filter('addr_line_1', operator, value)
            | _get_filter('addr_line_2', operator, value)
            | _get_filter('addr_line_3', operator, value))

    model = _get_model_by_field(field)

    value = value.lower()
    if model:
        Field = getattr(model, field)
        # TODO: we should sanitize the values
        if operator == 'contains':
            return Field.ilike('%' + value + '%')
        elif operator == 'exact':
            return Field.ilike(value)
        elif operator == 'endswith':
            return Field.ilike('%' + value)
        elif operator == 'startswith':
            return Field.ilike(value + '%')
        elif operator == 'wildcard':
            return Field.ilike(value)
        else:
            raise Exception('invalid operator: {}'.format(operator))
    else:
        raise Exception('invalid field: {}'.format(field))


def _get_sort_field(field_name):

    model = _get_model_by_field(field_name)
    if model:
        return getattr(model, field_name)
    else:
        raise Exception('invalid sort field: {}'.format(field_name))


def _get_corporation_search_results(args):
    query = args.get("query")

    if not query:
        return "No search query was received", 400

    # TODO: move queries to model class.
    results = (
        Corporation.query
        .join(CorpName, Corporation.corp_num == CorpName.corp_num)
        # .join(CorpParty, Corporation.corp_num == CorpParty.corp_num)
        # .join(Office, Office.corp_num == Corporation.corp_num)
        # .join(Address, Office.mailing_addr_id == Address.addr_id)
        .with_entities(
            CorpName.corp_nme,
            Corporation.corp_num,
            # Corporation.transition_dt,
            # Address.addr_line_1,
            # Address.addr_line_2,
            # Address.addr_line_3,
            # Address.postal_cd,
            # Address.city,
            # Address.province,
        )
        # .filter(Office.end_event_id == None)
        # .filter(CorpName.end_event_id == None)
    )

    results = results.filter(
        (Corporation.corp_num == query) |
        (CorpName.corp_nme.ilike('%' + query + '%'))
        # (CorpParty.first_nme.contains(query)) |
        # (CorpParty.last_nme.contains(query)))
    )

    return results


def _get_corpparty_search_results(args):
    """
    Querystring parameters as follows:

    You may provide query=<string> for a simple search, OR any number of querystring triples such as

    field=ANY_NME|first_nme|last_nme|<any column name>
    &operator=exact|contains|startswith|endswith
    &value=<string>
    &sort_type=asc|desc
    &sort_value=ANY_NME|first_nme|last_nme|<any column name>
    &additional_cols=address|active|none

    For example, to get everyone who has any name that starts with 'Sky', or last name must be exactly 'Little', do:
    curl "http://localhost/person/search/?field=ANY_NME&operator=startswith&value=Sky&field=last_nme&operator=exact&value=Little&mode=ALL"
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

    # Zip the lists, so ('last_nme', 'first_nme') , ('contains', 'exact'), ('Sky', 'Apple') => (('last_nme', 'contains', 'Sky'), ('first_nme', 'exact', 'Apple'))
    clauses = list(zip(fields, operators, values))

    # TODO: move queries to model class.
            # TODO: we no longer need this as we want to show all types.
            #.filter(CorpParty.party_typ_cd.in_(['FIO', 'DIR','OFF']))\

    results = (CorpParty.query
            # .filter(CorpParty.end_event_id == None)
            # .filter(CorpName.end_event_id == None)
            # .join(Corporation, Corporation.corp_num == CorpParty.corp_num)\
            # .join(CorpState, CorpState.corp_num == CorpParty.corp_num)\
            # .join(CorpOpState, CorpOpState.state_typ_cd == CorpState.state_typ_cd)\
            # .join(CorpName, Corporation.corp_num == CorpName.corp_num)\
            # .join(Address, CorpParty.mailing_addr_id == Address.addr_id)
            .add_columns(
                CorpParty.corp_party_id,
                CorpParty.first_nme,
                CorpParty.middle_nme,
                CorpParty.last_nme,
                CorpParty.appointment_dt,
                CorpParty.cessation_dt,
                CorpParty.corp_num,
                CorpParty.party_typ_cd,
                # Corporation.corp_num,
                # CorpName.corp_nme,
                # Address.addr_line_1,
                # Address.addr_line_2,
                # Address.addr_line_3,
                # Address.postal_cd,
                # Address.city,
                # Address.province,
                # CorpOpState.state_typ_cd,
                # CorpOpState.full_desc,
            ))

    results = _add_additional_cols_to_search_query(args, results)

    # Simple mode - return reasonable results for a single search string:
    if query:
        #results = results.filter((Corporation.corp_num == query) | (CorpParty.first_nme.contains(query)) | (CorpParty.last_nme.contains(query)))
        results = results.filter(CorpParty.first_nme.ilike(query) | CorpParty.last_nme.ilike(query) | CorpParty.middle_nme.ilike(query))
        # Advanced mode - return precise results for a set of clauses.
    elif clauses:

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
        results = results.order_by(CorpParty.last_nme, CorpParty.corp_num)
    else:
        field = _get_sort_field(sort_value)

        if sort_type == 'desc':
            results = results.order_by(desc(field))
        else:
            results = results.order_by(field)

    # TODO: uncomment
    #raise Exception(results.statement.compile())
    return results

def _normalize_addr(id):
    if not id:
        return ''

    address = Address.query.filter(Address.addr_id == id).add_columns(
        Address.addr_line_1,
        Address.addr_line_2,
        Address.addr_line_3,
        Address.postal_cd,
        Address.city,
        Address.province,
        Address.country_typ_cd,
        ).one()[0]

    def fn(accumulator, s):
        if s:
            return (accumulator or '') + ', ' + (s or '')
        else:
            return accumulator or ''

    return reduce(fn, [address.addr_line_1, address.addr_line_2, address.addr_line_3, address.city, address.province, address.country_typ_cd])

def _format_office_typ_cd(office_typ_cd):
    if office_typ_cd == "RG":
        return "Registered"
    elif office_typ_cd == "RC":
        return "Records"

# if __name__ == '__main__':
#     app = create_app()
#     app.run(host='0.0.0.0')
