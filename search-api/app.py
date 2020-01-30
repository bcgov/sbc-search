from flask import Flask, jsonify
from models import Corporation, CorpParty, app


@app.route('/')
def hello():
    return "Welcome to the director search API.s"


@app.route('/search/<query>/<page>/')
def search(query, page):
    results = Corporation.query\
        .join(CorpParty, Corporation.CORP_NUM == CorpParty.CORP_NUM)\
            .filter((Corporation.CORP_NUM == query) | (CorpParty.FIRST_NME.contains(query)) | (CorpParty.LAST_NME.contains(query))) \
            .paginate(int(page), 20, False)
    return jsonify({
        'results': [row.as_dict() for row in results.items]
    })
    # results = Corporation.query.filter_by(CORP_NUM=query)
    # return jsonify({
    #     'results': [row.as_dict() for row in results]
    # })


@app.route('/person/<id>')
def person(id):
    results = CorpParty.query.filter_by(CORP_PARTY_ID=int(id))
    if results.count() > 0:
        print(str(results[0].CORP_PARTY_ID))
        return jsonify(results[0].as_dict())
    return {}


@app.route('/corporation/<id>')
def corporation(id):
    results = Corporation.query.filter_by(CORP_NUM=id)
    if results.count() > 0:
        print(str(results[0]))
        return jsonify(results[0].as_dict())
    return {}


if __name__ == '__main__':
    app.run(host='0.0.0.0')