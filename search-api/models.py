
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@db/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Corporation(db.Model):
    __tablename__ = 'CORPORATION'
    """
    CORPORATION                    CORP_NUM                       VARCHAR2                       10                             2206759
    CORPORATION                    CORP_FROZEN_TYP_CD             CHAR                           1                              819
    CORPORATION                    CORP_TYP_CD                    VARCHAR2                       3                              2206759
    CORPORATION                    RECOGNITION_DTS                DATE                           7                              2111082
    CORPORATION                    LAST_AR_FILED_DT               DATE                           7                              1025542
    CORPORATION                    TRANSITION_DT                  DATE                           7                              240802
    CORPORATION                    BN_9                           VARCHAR2                       9                              1179842
    CORPORATION                    BN_15                          VARCHAR2                       15                             1179165
    CORPORATION                    ACCESSION_NUM                  VARCHAR2                       10                             941
    CORPORATION                    CORP_PASSWORD                  VARCHAR2                       300                            795500
    CORPORATION                    PROMPT_QUESTION                VARCHAR2                       100                            573423
    CORPORATION                    ADMIN_EMAIL                    VARCHAR2                       254                            703636
    CORPORATION                    SEND_AR_IND                    VARCHAR2                       1                              1642638
    CORPORATION                    TILMA_INVOLVED_IND             VARCHAR2                       1                              2196814
    CORPORATION                    TILMA_CESSATION_DT             DATE                           7                              4050
    CORPORATION                    FIRM_LAST_IMAGE_DATE           DATE                           7                              51550
    CORPORATION                    OS_SESSION                     db.Integer                         22                             420543
    CORPORATION                    LAST_AGM_DATE                  DATE                           7                              48416
    CORPORATION                    FIRM_LP_XP_TERMINATION_DATE    DATE                           7                              7443
    CORPORATION                    LAST_LEDGER_DT                 DATE                           7                              1
    CORPORATION                    AR_REMINDER_OPTION             VARCHAR2                       10                             69086
    CORPORATION                    AR_REMINDER_DATE               VARCHAR2                       20                             67640
    CORPORATION                    TEMP_PASSWORD                  VARCHAR2                       300                            3582
    CORPORATION                    TEMP_PASSWORD_EXPIRY_DATE      DATE                           7                              3582
    """

    CORP_NUM = db.Column(db.String(10), primary_key=True, unique=True)
    CORP_FROZEN_TYP_CD = db.Column(db.String(1))
    CORP_TYP_CD = db.Column(db.String(3))
    RECOGNITION_DTS = db.Column(db.Date)
    LAST_AR_FILED_DT = db.Column(db.Date)
    TRANSITION_DT = db.Column(db.Date)
    BN_9 = db.Column(db.String(9))
    BN_15 = db.Column(db.String(15))
    ACCESSION_NUM = db.Column(db.String(10))
    # CORP_PASSWORD = db.Column(db.String(300))
    # PROMPT_QUESTION = db.Column(db.String(100))
    ADMIN_EMAIL = db.Column(db.String(254))
    SEND_AR_IND = db.Column(db.String(1))
    TILMA_INVOLVED_IND = db.Column(db.String(1))
    TILMA_CESSATION_DT = db.Column(db.Date)
    FIRM_LAST_IMAGE_DATE = db.Column(db.Date)
    OS_SESSION = db.Column(db.Integer)
    LAST_AGM_DATE = db.Column(db.Date)
    FIRM_LP_XP_TERMINATION_DATE = db.Column(db.Date)
    LAST_LEDGER_DT = db.Column(db.Date)
    AR_REMINDER_OPTION = db.Column(db.String(10))
    AR_REMINDER_DATE = db.Column(db.String(20))
    # TEMP_PASSWORD = db.Column(db.String(300))
    # TEMP_PASSWORD_EXPIRY_DATE = db.Column(db.Date)

    def __repr__(self):
        return 'corp num: {}'.format(self.CORP_NUM)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class CorpParty(db.Model):
    __tablename__ = 'CORP_PARTY'
    """
    CORP_PARTY                     CORP_PARTY_ID                  db.Integer                         22                             11748880
    CORP_PARTY                     MAILING_ADDR_ID                db.Integer                         22                             8369745
    CORP_PARTY                     DELIVERY_ADDR_ID               db.Integer                         22                             7636885
    CORP_PARTY                     CORP_NUM                       VARCHAR2                       10                             11748884
    CORP_PARTY                     PARTY_TYP_CD                   CHAR                           3                              11748884
    CORP_PARTY                     START_EVENT_ID                 db.Integer                         22                             11748884
    CORP_PARTY                     END_EVENT_ID                   db.Integer                         22                             6194691
    CORP_PARTY                     PREV_PARTY_ID                  db.Integer                         22                             3623071
    CORP_PARTY                     CORR_TYP_CD                    CHAR                           1                              230615
    CORP_PARTY                     LAST_REPORT_DT                 DATE                           7                              50
    CORP_PARTY                     APPOINTMENT_DT                 DATE                           7                              3394297
    CORP_PARTY                     CESSATION_DT                   DATE                           7                              3071988
    CORP_PARTY                     LAST_NME                       VARCHAR2                       30                             11397162
    CORP_PARTY                     MIDDLE_NME                     VARCHAR2                       30                             2773092
    CORP_PARTY                     FIRST_NME                      VARCHAR2                       30                             11392744
    CORP_PARTY                     BUSINESS_NME                   VARCHAR2                       150                            369824
    CORP_PARTY                     BUS_COMPANY_NUM                VARCHAR2                       15                             108582
    CORP_PARTY                     EMAIL_ADDRESS                  VARCHAR2                       254                            10442
    CORP_PARTY                     CORP_PARTY_SEQ_NUM             db.Integer                         22                             27133
    CORP_PARTY                     OFFICE_NOTIFICATION_DT         DATE                           7                              8380
    CORP_PARTY                     PHONE                          VARCHAR2                       30                             4306
    CORP_PARTY                     REASON_TYP_CD                  VARCHAR2                       3                              0
    """
    CORP_PARTY_ID = db.Column(db.Integer, primary_key=True)
    MAILING_ADDR_ID = db.Column(db.Integer)
    DELIVERY_ADDR_ID = db.Column(db.Integer)
    CORP_NUM = db.Column(db.String(10))
    PARTY_TYP_CD = db.Column(db.String(3))
    START_EVENT_ID = db.Column(db.Integer)
    END_EVENT_ID = db.Column(db.Integer)
    PREV_PARTY_ID = db.Column(db.Integer)
    CORR_TYP_CD = db.Column(db.String(1))
    LAST_REPORT_DT = db.Column(db.Date)
    APPOINTMENT_DT = db.Column(db.Date)
    CESSATION_DT = db.Column(db.Date)
    LAST_NME = db.Column(db.String(30))
    MIDDLE_NME = db.Column(db.String(30))
    FIRST_NME = db.Column(db.String(30))
    BUSINESS_NME = db.Column(db.String(150))
    BUS_COMPANY_NUM = db.Column(db.String(15))
    EMAIL_ADDRESS = db.Column(db.String(254))
    CORP_PARTY_SEQ_NUM = db.Column(db.Integer)
    OFFICE_NOTIFICATION_DT = db.Column(db.Date)
    PHONE = db.Column(db.String(30))
    REASON_TYP_CD = db.Column(db.String(3))
