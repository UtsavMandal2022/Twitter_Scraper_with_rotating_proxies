from flask import Flask, render_template, jsonify
from newscript import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_topics', methods=['GET'])
def fetch_topics():
    result = fetch_trending_topics()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
