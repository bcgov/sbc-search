from flask import Flask, jsonify
from models import Corporation, app


@app.route('/')
def hello():
    return "Welcome to the director search API.s"


@app.route('/search/<query>')
def search(query):
    results = Corporation.query.filter_by(CORP_NUM=query)
    return jsonify({
        'results': [row.as_dict() for row in results]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0')
