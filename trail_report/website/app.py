from __future__ import division
from math import sqrt
from flask import Flask, render_template, request, jsonify
from ..build_model.make_all_predictions import get_data, TrailPred, get_pickle, load_databases
from ..build_model.trail_names import Trails
import pickle
import ast


app = Flask(__name__)

print("Est. loading time: 2 minutes")
tp = get_pickle()
print("Almost there.")
df_init, df_trail, weather, weather_dist = load_databases()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', trails=Trails)


@app.route('/solve', methods=['POST'])
def solve():
    """Collect data and return in json form"""
    user_data = request.json
    hike, date = user_data['hike'], user_data['hike_date']
    snow_prob, trail_prob, bugs_prob, road_prob, snow_text, trail_text, bugs_text, road_text = _get_prediction(
        hike, date)
    return jsonify({'snow_prob': snow_prob,
                    'trail_prob': trail_prob,
                    'bugs_prob': bugs_prob,
                    'road_prob': road_prob,
                    'snow_text': str(snow_text),
                    'trail_text': str(trail_text),
                    'bugs_text': str(bugs_text),
                    'road_text': str(road_text)
                    })


def _get_prediction(hike, date):
    """Prep data and get predictions on user input."""
    X_test, Text_X_text = get_data(
        hike, date, df_init, df_trail, weather, weather_dist)
    pred = tp.predict(X_test)
    tp.predict_text(Text_X_text, df_init, hike)
    # snow_text = tp.all_text['condition|snow']
    # trail_text = tp.all_text['condition|trail']
    # bugs_text= tp.all_text['condition|bugs']
    # road_text = tp.all_text['condition|road']
    snow_text = get_relivant_text(tp.all_text['condition|snow'])
    trail_text = get_relivant_text(tp.all_text['condition|trail'])
    bugs_text = get_relivant_text(tp.all_text['condition|bugs'])
    road_text = get_relivant_text(tp.all_text['condition|road'])
    return ("{0:.0f}%".format(float(pred['condition|snow'][:, 1][0]) * 100),
            "{0:.0f}%".format(float(pred['condition|trail'][:, 1][0]) * 100),
            "{0:.0f}%".format(float(pred['condition|bugs'][:, 1][0]) * 100),
            "{0:.0f}%".format(float(pred['condition|road'][:, 1][0]) * 100),
            snow_text, trail_text, bugs_text, road_text
            )


def get_relivant_text(reports):
    """Clean text from dictionary."""
    returns = ''
    if isinstance(reports, str):
        returns = reports
    else:
        for year, text in reports.items():
            returns += f"On {year} Reports say: <br /> <br />"
            for part in text:
                returns += u'\u2022 '
                returns += part
                returns += '<br />'
            returns += '<br />'
    return returns


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
    # hike = 'Rattlesnake Ledge'
    # date = '05/22/18'
    # snow_prob, trail_prob, bugs_prob, road_prob,snow_text, trail_text, bugs_text, road_text = _get_prediction(hike,date)
    # print (snow_prob, trail_prob, bugs_prob, road_prob,'snow_text', snow_text, 'trail_text', trail_text, 'bugs_text', bugs_text, 'road_text', road_text)
