from flask import Flask, request, jsonify
from functools import reduce
from models import (
    Corporation, 
    CorpParty, 
    CorpName, 
    Address, 
    OfficesHeld, 
    OfficerType, 
    app,
)


@app.route('/')
def hello():
    return "Welcome to the director search API.s"


def _get_filter(field, operator, value):
    
    if field == 'ANY_NME':
        return (_get_filter('FIRST_NME', operator, value)
            | _get_filter('MIDDLE_NME', operator, value)
            | _get_filter('LAST_NME', operator, value))

    Field = getattr(CorpParty, field)
    if operator == 'contains':
        return Field.contains(value)
    elif operator == 'exact':
        return Field == value
    elif operator == 'endswith':
        return Field.endswith(value)
    elif operator == 'startswith':
        return Field.startswith(value)
    else:
        raise Exception('invalid operator: {}'.format(operator))

@app.route('/corporation/search/')
def corporation_search():

    args = request.args

    page = 1
    if "page" in args:
        page = int(args.get("page"))

    if "query" not in args:
        return "No search query was received", 400

    query = args["query"]

    # TODO: move queries to model class.
    results = Corporation.query\
        .join(CorpParty, Corporation.CORP_NUM == CorpParty.CORP_NUM)\
        .join(CorpName, Corporation.CORP_NUM == CorpName.CORP_NUM)
    
    results = results.filter(
        (Corporation.CORP_NUM == query) |
        (CorpName.CORP_NME.contains(query)) |
        (CorpParty.FIRST_NME.contains(query)) |
        (CorpParty.LAST_NME.contains(query)))
    
    results = results.paginate(int(page), 20, False)
    
    # TODO: include corpname and corpparties in serialized child using Marshmallow
    return jsonify({
        'results': [row.as_dict() for row in results.items]
    })


@app.route('/person/search/')
def corpparty_search():

    args = request.args

    page = 1
    if "page" in args:
        page = int(args.get("page"))


    query = args.get("query")

    fields = args.getlist('field')
    operators = args.getlist('operator')
    values = args.getlist('value')
    mode = args.get('mode')

    if query and len(fields) > 0:
        raise Exception("use simple query or advanced. don't mix")

    if len(fields) != len(operators) or len(operators) != len(values):
        raise Exception("mismatched query param lengths: fields:{} operators:{} values:{}".format(
            len(fields),
            len(operators),
            len(values)))

    grps = list(zip(fields, operators, values))

    # TODO: move queries to model class.

    results = CorpParty.query\
            .join(Corporation, Corporation.CORP_NUM == CorpParty.CORP_NUM)\
            .join(CorpName, Corporation.CORP_NUM == CorpName.CORP_NUM)\
            .join(Address, CorpParty.MAILING_ADDR_ID == Address.ADDR_ID)\
            .add_columns(\
                CorpParty.CORP_PARTY_ID, 
                CorpParty.FIRST_NME, 
                CorpParty.MIDDLE_NME,
                CorpParty.LAST_NME,
                CorpParty.APPOINTMENT_DT,
                CorpParty.CESSATION_DT,
                Corporation.CORP_NUM,
                CorpName.CORP_NME,
                Address.ADDR_LINE_1,
            )
 
    if query:
        results = results.filter((Corporation.CORP_NUM == query) | (CorpParty.FIRST_NME.contains(query)) | (CorpParty.LAST_NME.contains(query)))
    elif grps:
        if mode == 'ALL':
            def fn(accumulator, s):
                return accumulator & _get_filter(*s)
        else:
            def fn(accumulator, s):
                return accumulator | _get_filter(*s)
        filter_grp = reduce(
            fn,
            grps[1:],
            _get_filter(*grps[0])
            )
        results = results.filter(filter_grp)
    else:
        pass
    results = results.paginate(int(page), 20, False)

    corp_parties = []
    for row in results.items:
        result_dict = {}

        result_dict['CORP_PARTY_ID'] = row[1]
        result_dict['FIRST_NME'] = row[2]
        result_dict['MIDDLE_NME'] = row[3]
        result_dict['LAST_NME'] = row[4]
        result_dict['APPOINTMENT_DT'] = row[5]
        result_dict['CESSATION_DT'] = row[6]
        result_dict['CORP_NUM'] = row[7]
        result_dict['CORP_NME'] = row[8]
        result_dict['ADDR_LINE_1'] = row[9]

        corp_parties.append(result_dict)

    
    return jsonify({'results': corp_parties})


@app.route('/person/<id>')
def person(id):
    results = CorpParty.query.filter_by(CORP_PARTY_ID=int(id))
    if results.count() > 0:
        return jsonify(results[0].as_dict())
    return {}


@app.route('/person/officesheld/<corppartyid>')
def officesheld(corppartyid):
    results = OfficerType.query\
            .join(OfficesHeld, OfficerType.OFFICER_TYP_CD==OfficesHeld.OFFICER_TYP_CD)\
            .join(CorpParty, OfficesHeld.CORP_PARTY_ID == CorpParty.CORP_PARTY_ID)\
            .join(Address, CorpParty.MAILING_ADDR_ID == Address.ADDR_ID)\
            .add_columns(\
                CorpParty.CORP_PARTY_ID, 
                OfficerType.OFFICER_TYP_CD,
                OfficerType.SHORT_DESC,
                CorpParty.APPOINTMENT_DT,
                Address.ADDR_LINE_1,
            )\
            .filter(CorpParty.CORP_PARTY_ID==int(corppartyid))
    
    offices = []
    for row in results:
        result_dict = {}

        result_dict['CORP_PARTY_ID'] = row[1]
        result_dict['OFFICER_TYP_CD'] = row[2]
        result_dict['SHORT_DESC'] = row[3]
        result_dict['APPOINTMENT_DT'] = row[4]
        result_dict['ADDR_LINE_1'] = row[5]

        offices.append(result_dict)
    
    return jsonify({'results': offices})


@app.route('/corporation/<id>')
def corporation(id):
    results = Corporation.query.filter_by(CORP_NUM=id)
    if results.count() > 0:
        return jsonify(results[0].as_dict())
    return {}


if __name__ == '__main__':
    app.run(host='0.0.0.0')
