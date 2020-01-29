from flask import Flask, jsonify
from models import Corporation, app


@app.route('/')
def hello():
    return "Welcome to the director search API."


@app.route('/search/<query>')
def search(query):
    results = Corporation.query.filter_by(CORP_NUM=query)
    return jsonify({
        'results': [row.as_dict() for row in results]
    })

@app.route('/person/<id>')
def person(id):
    results = CorpParty.query.filter_by(CORP_PARTY_ID=int(id))
    return jsonify({
        'results': results[0].as_dict()
    })

@app.route('/corporation/<id>')
def corporation(id):
    results = Corporation.query.filter_by(CORP_NUM=id)
    return jsonify({
        'results': results[0].as_dict()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0')
