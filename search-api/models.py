from sqlalchemy import Column, Date, String, Integer, func  
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Corporation(Base):  
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
    CORPORATION                    OS_SESSION                     NUMBER                         22                             420543
    CORPORATION                    LAST_AGM_DATE                  DATE                           7                              48416
    CORPORATION                    FIRM_LP_XP_TERMINATION_DATE    DATE                           7                              7443
    CORPORATION                    LAST_LEDGER_DT                 DATE                           7                              1
    CORPORATION                    AR_REMINDER_OPTION             VARCHAR2                       10                             69086
    CORPORATION                    AR_REMINDER_DATE               VARCHAR2                       20                             67640
    CORPORATION                    TEMP_PASSWORD                  VARCHAR2                       300                            3582
    CORPORATION                    TEMP_PASSWORD_EXPIRY_DATE      DATE                           7                              3582
    """

    CORP_NUM = Column(String, length=10, primary_key=True)
    CORP_FROZEN_TYP_CD = Column(String, length=1)
    CORP_TYP_CD = Column(String, length=3)
    RECOGNITION_DTS = Column(Date)
    LAST_AR_FILED_DT = Column(Date)
    TRANSITION_DT = Column(Date)
    BN_9 = Column(String, length=9)
    BN_15 = Column(String, length=15)
    ACCESSION_NUM = Column(String, length=10)
    CORP_PASSWORD = Column(String, length=300)
    PROMPT_QUESTION = Column(String, length=100)
    ADMIN_EMAIL = Column(String, length=254)
    SEND_AR_IND = Column(String, length=1)
    TILMA_INVOLVED_IND = Column(String, length=1)
    TILMA_CESSATION_DT = Column(Date)
    FIRM_LAST_IMAGE_DATE = Column(Date)
    OS_SESSION = Column(Number)
    LAST_AGM_DATE = Column(Date)
    FIRM_LP_XP_TERMINATION_DATE = Column(Date)
    LAST_LEDGER_DT = Column(Date)
    AR_REMINDER_OPTION = Column(String, length=10)
    AR_REMINDER_DATE = Column(String, length=20)
    TEMP_PASSWORD = Column(String, length=300)
    TEMP_PASSWORD_EXPIRY_DATE = Column(Date)
    def __repr__(self):
        return 'corp num: {}'.format(self.CORP_NUM)

class CorpParty(Base):  
    __tablename__ = 'CORP_PARTY'
    """
    CORP_PARTY                     CORP_PARTY_ID                  NUMBER                         22                             11748880
    CORP_PARTY                     MAILING_ADDR_ID                NUMBER                         22                             8369745
    CORP_PARTY                     DELIVERY_ADDR_ID               NUMBER                         22                             7636885
    CORP_PARTY                     CORP_NUM                       VARCHAR2                       10                             11748884
    CORP_PARTY                     PARTY_TYP_CD                   CHAR                           3                              11748884
    CORP_PARTY                     START_EVENT_ID                 NUMBER                         22                             11748884
    CORP_PARTY                     END_EVENT_ID                   NUMBER                         22                             6194691
    CORP_PARTY                     PREV_PARTY_ID                  NUMBER                         22                             3623071
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
    CORP_PARTY                     CORP_PARTY_SEQ_NUM             NUMBER                         22                             27133
    CORP_PARTY                     OFFICE_NOTIFICATION_DT         DATE                           7                              8380
    CORP_PARTY                     PHONE                          VARCHAR2                       30                             4306
    CORP_PARTY                     REASON_TYP_CD                  VARCHAR2                       3                              0
    """
    CORP_PARTY_ID = Column(Number)
    MAILING_ADDR_ID = Column(Number)
    DELIVERY_ADDR_ID = Column(Number)
    CORP_NUM = Column(String, length=10)
    PARTY_TYP_CD = Column(String, length=3)
    START_EVENT_ID = Column(Number)
    END_EVENT_ID = Column(Number)
    PREV_PARTY_ID = Column(Number)
    CORR_TYP_CD = Column(String, length=1)
    LAST_REPORT_DT = Column(Date)
    APPOINTMENT_DT = Column(Date)
    CESSATION_DT = Column(Date)
    LAST_NME = Column(String, length=30)
    MIDDLE_NME = Column(String, length=30)
    FIRST_NME = Column(String, length=30)
    BUSINESS_NME = Column(String, length=150)
    BUS_COMPANY_NUM = Column(String, length=15)
    EMAIL_ADDRESS = Column(String, length=254)
    CORP_PARTY_SEQ_NUM = Column(Number)
    OFFICE_NOTIFICATION_DT = Column(Date)
    PHONE = Column(String, length=30)
    REASON_TYP_CD = Column(String, length=3)