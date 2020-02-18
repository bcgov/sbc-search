from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://User_OxpgHxo0:T4QDb1YNVesbqOEfxYp3@172.19.0.1:15432/BC_REGISTRIES'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@db/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class BaseModel(db.Model):
    __abstract__ = True
    __table_args__ = {'quote':False, 'schema': 'bc_registries'} 
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Address(BaseModel):
    __tablename__ = "address"
    """
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
    start_event_id = db.Column(db.Integer, primary_key=True)
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
    CORP_PARTY                     party_type_cd                   CHAR                           3                              11748884
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
    party_type_cd = db.Column(db.String(3))
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
