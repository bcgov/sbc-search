from search_api.models.base import db


# Compare original COBRS system performance.
COBRS_SQL = '''SELECT
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
WHERE UPPER(LAST_NME) LIKE 'JOHN'
    #AND PARTY_TYP_CD IN ('FIO', 'DIR','OFF')
    AND P.END_EVENT_ID IS NULL
    AND P.CORP_NUM = S.CORP_NUM
    AND S.END_EVENT_ID IS NULL
    AND S.STATE_TYP_CD = OS.STATE_TYP_CD
    AND S.CORP_NUM = C.CORP_NUM
    AND C.CORP_TYP_CD = CT.CORP_TYP_CD
    AND ROWNUM <= 11165
ORDER BY UPPER(LAST_NME)
#, UPPER(FIRST_NME), STATUS,CORP_CLASS,CORP_NUM DESC
'''

# Director search sql example.
DS_OPT = '''
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
'''

DS_REAL = '''
SELECT corp_party.corp_party_id,
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
FROM   corp_party
       join corporation
         ON corporation.corp_num = corp_party.corp_num
       join corp_state
         ON corp_state.corp_num = corp_party.corp_num
       left outer join corp_name
                    ON corporation.corp_num = corp_name.corp_num
       left outer join address
                    ON corp_party.mailing_addr_id = address.addr_id
WHERE  corp_party.end_event_id IS NULL
       AND corp_state.end_event_id IS NULL
       AND corp_name.end_event_id IS NULL
       AND corp_name.corp_name_typ_cd IN (
           'NB', 'CO' )
       AND Upper(corp_party.last_nme) LIKE 'CLARK'
       AND ROWNUM <= 1000
ORDER  BY Upper(corp_party.last_nme) DESC

'''

if __name__ == "__main__":
    """
    Test performance of raw queries.
    """
    from search_api import create_app
    import time
    app = create_app('development')

    for sql in [DS_OPT, DS_OPT, DS_OPT, DS_REAL, DS_REAL, DS_REAL]:
        with app.app_context():
            sql = '\n'.join([s for s in sql.split("\n") if '#' not in s])
            t=time.time()
            rs = db.session.execute(sql)
            print('end query time', time.time()-t)
            print('results',rs)
            count = 0
            for row in rs:
                count += 1
                # print(row)
            print('count', count)
