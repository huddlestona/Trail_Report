from __future__ import division
from math import sqrt
from flask import Flask, render_template, request, jsonify
from make_prediction import Make_Prediction
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('test.html')


@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    hike, hike_date = user_data['hike'], user_data['hike_date']
    root_1= _get_prediction(hike, hike_date)
    return jsonify({'root_1': root_1})


def _get_prediction(hike, hike_date):
    condition = 'condition|snow'
    pred = Make_Prediction(hike,hike_date,condition)
    return pred


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)