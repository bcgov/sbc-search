from flask import Flask, request, jsonify
from models import Corporation, CorpParty, app


@app.route('/')
def hello():
    return "Welcome to the director search API.s"


@app.route('/corporation/search/')
def corporation_search():

    args = request.args

    page = 1
    if "page" in args:
        page = int(args.get("page"))

    if "query" not in args:
        return "No search query was received", 400
    query = args["query"]

    results = Corporation.query\
        .join(CorpParty, Corporation.CORP_NUM == CorpParty.CORP_NUM)\
            .filter((Corporation.CORP_NUM == query) | (CorpParty.FIRST_NME.contains(query)) | (CorpParty.LAST_NME.contains(query))) \
            .paginate(int(page), 20, False)
            
    return jsonify({
        'results': [row.as_dict() for row in results.items]
    })


@app.route('/person/search/')
def corpparty_search():

    args = request.args

    page = 1
    if "page" in args:
        page = int(args.get("page"))

    if "query" not in args:
        return "No search query was received", 400
    query = args["query"]

    results = CorpParty.query\
            .filter((CorpParty.FIRST_NME.contains(query)) | (CorpParty.LAST_NME.contains(query))) \
            .paginate(int(page), 20, False)
    
    return jsonify({
        'results': [row.as_dict() for row in results.items]
    })


@app.route('/person/<id>')
def person(id):
    results = CorpParty.query.filter_by(CORP_PARTY_ID=int(id))
    if results.count() > 0:
        return jsonify(results[0].as_dict())
    return {}


@app.route('/corporation/<id>')
def corporation(id):
    results = Corporation.query.filter_by(CORP_NUM=id)
    if results.count() > 0:
        return jsonify(results[0].as_dict())
    return {}


if __name__ == '__main__':
    app.run(host='0.0.0.0')