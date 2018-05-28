from __future__ import division
from math import sqrt
from flask import Flask, render_template, request, jsonify
from ..build_model.make_all_predictions import get_data, TrailPred, get_pickle
import pickle 


app = Flask(__name__)

# with open('tp.pkl','rb') as f:
#     tp = pickle.load(f)
tp = get_pickle()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    hike, date = user_data['hike'], user_data['hike_date']
    snow_prob,trail_prob,bugs_prob,road_prob = _get_prediction(hike, date)
    return jsonify({'snow_prob': snow_prob,'trail_prob': trail_prob,'bugs_prob': bugs_prob,'road_prob': road_prob})


def _get_prediction(hike, date):
    X_test = get_data(hike,date)
    pred = tp.predict(X_test)
    return ("{0:.0f}%".format(float(pred['condition|snow'][:,1][0])*100),
            "{0:.0f}%".format(float(pred['condition|trail'][:,1][0])*100),
            "{0:.0f}%".format(float(pred['condition|bugs'][:,1][0])*100),
            "{0:.0f}%".format(float(pred['condition|road'][:,1][0])*100))
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
