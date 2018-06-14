from __future__ import division
from math import sqrt
from flask import Flask, render_template, request, jsonify
from ..build_model.make_all_predictions import get_data, TrailPred, get_pickle,load_databases
from ..build_model.trail_names import Trails
import pickle


app = Flask(__name__)

Print("Est. loading time: 10 minutes")
tp = get_pickle()
Print("Almost there.")
df_init, df_trail, weather, weather_dist = load_databases()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', trails=Trails)


@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    hike, date = user_data['hike'], user_data['hike_date']
    snow_prob, trail_prob, bugs_prob, road_prob,snow_text, trail_text, bugs_text, road_text = _get_prediction(hike, date)
    return jsonify({'snow_prob': snow_prob,
                    'trail_prob': trail_prob,
                    'bugs_prob': bugs_prob,
                    'road_prob': road_prob,
                    'snow_text': snow_text,
                    'trail_text': trail_text,
                    'bugs_text': bugs_text,
                    'road_text': road_text
                    })


def _get_prediction(hike, date):
    X_test, Text_X_text = get_data(hike, date, df_init, df_trail, weather, weather_dist)
    pred = tp.predict(X_test)
    tp.predict_text(Text_X_text)
    tp.get_all_text(df_init)
    snow_text = get_relivant_text(tp.all_text['condition|snow'])
    trail_text = get_relivant_text(tp.all_text['condition|trail'])
    bugs_text= get_relivant_text(tp.all_text['condition|bugs'])
    road_text = get_relivant_text(tp.all_text['condition|road'])
    return ("{0:.0f}%".format(float(pred['condition|snow'][:, 1][0]) * 100),
            "{0:.0f}%".format(float(pred['condition|trail'][:, 1][0]) * 100),
            "{0:.0f}%".format(float(pred['condition|bugs'][:, 1][0]) * 100),
            "{0:.0f}%".format(float(pred['condition|road'][:, 1][0]) * 100),
            snow_text, trail_text, bugs_text, road_text
            )

def get_relivant_text(reports):
    returns = ''
    for group in reports:
        for year,parts in group.items():
            returns += f"On {year} Reports say: \n \n"
            for sent in parts:
                returns += u'\u2022 '
                returns += sent
                returns += '\n'
            returns += '\n'
    return returns

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
    # hike = 'Mount Rose'
    # date = '05/22/18'
    # snow_prob, trail_prob, bugs_prob, road_prob,snow_text, trail_text, bugs_text, road_text = _get_prediction(hike,date)
    # print (snow_prob, trail_prob, bugs_prob, road_prob,snow_text, trail_text, bugs_text, road_text)