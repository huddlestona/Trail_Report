from __future__ import division
from math import sqrt
from flask import Flask, render_template, request, jsonify
from Modules.make_all_predictions import *
app = Flask(__name__)

with open('Modules/tp.pkl','rb') as f:
    tp = pickle.load(f)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    hike, date = user_data['hike'], user_data['hike_date']
    root_1,root_2,root_3,root_4= _get_prediction(hike, date)
    return jsonify({'root_1': root_1,'root_2': root_2,'root_3': root_3,'root_4': root_4})


def _get_prediction(hike, date):
    X_test = get_data(hike,date)
    pred = tp.predict(X_test)
    return (pred['condition|snow'][:,1][0],
            pred['condition|trail'][:,1][0],
            pred['condition|bugs'][:,1][0],
            pred['condition|road'][:,1][0])
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
