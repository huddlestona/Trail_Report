from __future__ import division
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from math import sqrt
from flask import Flask, render_template, request, jsonify
from make_any_prediction import New_Input
app = Flask(__name__)

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
    conditions = ['condition|snow', 'condition|trail','condition|bugs','condition|road']
    #snow
    snow =  New_Input(hike,date,'condition|snow')
    snow.prep_input()
    snow_prob = snow.make_prediction()
    snow_words = snow.get_top_text()
    #trail
    trail =  New_Input(hike,date,'condition|trail')
    trail.prep_input()
    trail_prob = trail.make_prediction()
    trail_words = trail.get_top_text()
    #Bugs
    bugs =  New_Input(hike,date,'condition|bugs')
    bugs.prep_input()
    bugs_prob = bugs.make_prediction()
    bugs_words = bugs.get_top_text()
    #road
    road =  New_Input(hike,date,'condition|road')
    road.prep_input()
    road_prob = road.make_prediction()
    road_words = road.get_top_text()
    return snow_prob,trail_prob,bugs_prob,road_prob

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
