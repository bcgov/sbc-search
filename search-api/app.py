from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/')
def hello():
    return "Welcome to the director search API.s"


@app.route('/search/<query>')
def search(query):
    return jsonify({
        'result': query,
        'count': 1
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0')

