import time
import sys

from sqlalchemy import func
from sqlalchemy.sql import literal_column
from sqlalchemy.dialects import oracle
from werkzeug.datastructures import ImmutableMultiDict

from search_api import create_app
from search_api.models.base import db
from search_api.models.corp_party import CorpParty
from search_api.models.corporation import Corporation
from search_api.models.nickname import NickName

# Compare original COBRS system performance.
COBRS_SQL = """SELECT
       UPPER(LAST_NME)
      ,UPPER(FIRST_NME)
      ,P.CORP_NUM
      ,CASE  PARTY_TYP_CD       WHEN 'FIO' THEN 'OWNER'
                                WHEN 'DIR' THEN 'DIR'
                                ELSE 'OFF' END AS TITLE
    #   , CASE OS.OP_STATE_TYP_CD WHEN 'ACT' THEN 'A'
    #                             ELSE 'H' END AS STATUS
      ,CORP_PARTY_ID
      ,CORP_CLASS
  FROM CORP_PARTY P
      ,CORP_STATE S
      ,CORP_OP_STATE OS
      ,CORPORATION  C
      ,CORP_TYPE    CT
WHERE UPPER(FIRST_NME) LIKE 'JOHN'
    #AND PARTY_TYP_CD IN ('FIO', 'DIR','OFF')
    AND P.END_EVENT_ID IS NULL
    AND P.CORP_NUM = S.CORP_NUM
    AND S.END_EVENT_ID IS NULL
    AND S.STATE_TYP_CD = OS.STATE_TYP_CD
    AND S.CORP_NUM = C.CORP_NUM
    AND C.CORP_TYP_CD = CT.CORP_TYP_CD
    AND ROWNUM <= 165
ORDER BY UPPER(LAST_NME)
#, UPPER(FIRST_NME), STATUS,CORP_CLASS,CORP_NUM DESC
"""

# Director search sql example.
DS_OPT = """
SELECT
    corp_party.corp_party_id,
       corp_party.mailing_addr_id,
       corp_party.delivery_addr_id,
       corp_party.corp_num,
       corp_party.party_typ_cd,
       corp_party.start_event_id,
       corp_party.end_event_id,
       corp_party.prev_party_id,
       corp_party.corr_typ_cd,
       corp_party.last_report_dt,
       corp_party.appointment_dt,
       corp_party.cessation_dt,
       corp_party.last_nme,
       corp_party.middle_nme,
       corp_party.first_nme,
       corp_party.business_nme,
       corp_party.bus_company_num,
       corp_party.email_address,
       corp_party.corp_party_seq_num,
       corp_party.phone,
       corp_party.reason_typ_cd,
       corp_name.corp_nme,
       address.addr_line_1,
       address.addr_line_2,
       address.addr_line_3,
       address.postal_cd
FROM
    corp_party
    JOIN corporation ON corporation.corp_num = corp_party.corp_num
    JOIN corp_state ON corp_state.corp_num = corp_party.corp_num
    JOIN corp_op_state ON corp_op_state.state_typ_cd = corp_state.state_typ_cd
    LEFT OUTER JOIN corp_name ON corporation.corp_num = corp_name.corp_num
    LEFT OUTER JOIN address ON corp_party.mailing_addr_id = address.addr_id
WHERE upper(corp_party.last_nme) LIKE 'JOHN'
    AND corp_party.END_EVENT_ID IS NULL
    and corp_state.end_event_id is null
    and corp_name.end_event_id is null
    #AND ROWNUM <= 50
ORDER BY upper(corp_party.last_nme)
"""


def _benchmark(t, rs):
    """Benchmark utility"""
    if hasattr(rs, "statement"):
        oracle_dialect = oracle.dialect(max_identifier_length=30)
        raw_sql = str(rs.statement.compile(dialect=oracle_dialect))
        #print(raw_sql)

    count = 0
    for row in rs:
        if (count >= 50):
            break
        #print(row)
        count += 1
    print("raw query time:", time.time() - t, " number of results:", count)


def corporations():
    print("Search corporations")
    return Corporation.search_corporations(
        ImmutableMultiDict([("query", "countable"), ("page", "1"), ("sort_type", "dsc"), ("sort_value", "corpNme")])
    ).filter(
        literal_column("rownum") <= 500
    ).yield_per(50)


def corp_party_search():
    print("Search Corp Party")

    args = ImmutableMultiDict(
        [
            ("field", "firstNme"),
            ("operator", "exact"),
            ("value", "john"),
            ("mode", "ALL"),
            ("page", "1"),
            ("sort_type", "dsc"),
            ("sort_value", "lastNme"),
            ("additional_cols", "none"),
        ]
    )

    return CorpParty.search_corp_parties(args).filter(
        literal_column("rownum") <= 500
    ).yield_per(50)


def corp_party_similar_search():
    print("Search Corp Party by similar")

    args = ImmutableMultiDict(
        [
            ("field", "firstNme"),
            ("field", "lastNme"),
            ("operator", "similar"),
            ("operator", "exact"),
            ("value", "john"),
            ("value", "smith"),
            ("mode", "ALL"),
            ("additional_cols", "none"),
            ("page", "1"),
            ("sort_type", "dsc"),
            ("sort_value", "lastNme"),
        ]
    )

    return CorpParty.search_corp_parties(args).filter(
        literal_column("rownum") <= 500
    ).yield_per(50)

def corp_party_nickname_search():
    print("Search Corp Party by nickname")

    args = ImmutableMultiDict(
        [
            ("field", "firstNme"),
            ("field", "lastNme"),
            ("operator", "nicknames"),
            ("operator", "exact"),
            ("value", "john"),
            ("value", "smith"),
            ("mode", "ALL"),
            ("additional_cols", "none"),
            ("page", "1"),
            ("sort_type", "dsc"),
            ("sort_value", "lastNme"),
        ]
    )

    return CorpParty.search_corp_parties(args).filter(
        literal_column("rownum") <= 500
    ).yield_per(50)


def corp_party_2param_search():
    print("Corp party 2 params")
    args = ImmutableMultiDict(
        [
            ("field", "firstNme"),
            ("field", "lastNme"),
            ("operator", "startswith"),
            ("operator", "startswith"),
            ("value", "clark"),
            ("value", "van"),
            ("mode", "ALL"),
            ("additional_cols", "none"),
            ("page", "1"),
            ("sort_type", "dsc"),
            ("sort_value", "lastNme"),
        ]
    )
    return CorpParty.search_corp_parties(args).filter(
        literal_column("rownum") <= 500
    ).yield_per(50)


def corp_party_addr_search():
    print("Search Corp Party by Address:")

    args = ImmutableMultiDict(
        [
            ("field", "firstNme"),
            ("operator", "contains"),
            ("value", "john"),
            ("field", "addrLine1"),
            ("operator", "contains"),
            ("value", "main"),
            ("mode", "ALL"),
            ("page", "1"),
            ("sort_type", "dsc"),
            ("sort_value", "lastNme"),
            ("additional_cols", "none"),
        ]
    )

    return CorpParty.search_corp_parties(args).filter(
        literal_column("rownum") <= 500
    ).yield_per(50)

def corp_party_postal_cd_search():
    print("Search Corp Party by Postal Code:")
    # Notes -
    # Ideally we'd like an index of UPPER(TRIM(POSTAL_CD)) for address.
    # Instead, the implementation is to try the 2 common versions. Uppercase with a space and
    # uppercase without.
    args = ImmutableMultiDict(
        [
            ("field", "postalCd"),
            ("operator", "exact"),
            ("value", "V0H2B0"),
            ("mode", "ALL"),
            ("page", "1"),
            ("sort_type", "dsc"),
            ("sort_value", "lastNme"),
            ("additional_cols", "none"),
        ]
    )

    return CorpParty.search_corp_parties(args).filter(
        literal_column("rownum") <= 500
    ).yield_per(50)


def raw_sql(sql):
    print("Benchmark raw SQL")
    sql = "\n".join([s for s in sql.split("\n") if "#" not in s])
    return db.session.execute(sql)

SQL = '''
select 1 from corp_party
'''

if __name__ == "__main__":
    """
    Test performance of raw queries.
    """

    app = create_app("development")
    with app.app_context():
        for i in range(1):

            t = time.time()
            rs = raw_sql(SQL)
            _benchmark(t, rs)

            t = time.time()
            rs = raw_sql(COBRS_SQL)
            _benchmark(t, rs)

            t = time.time()
            rs = corp_party_addr_search()
            _benchmark(t, rs)
            
            t = time.time()
            rs = corp_party_search()
            _benchmark(t, rs)
            
            t = time.time()
            rs = corp_party_postal_cd_search()
            _benchmark(t, rs)
            
            t = time.time()
            rs = corp_party_nickname_search()
            _benchmark(t, rs)

            t = time.time()
            rs = corp_party_similar_search()
            _benchmark(t, rs)

            t = time.time()
            rs = corporations()
            _benchmark(t, rs)
