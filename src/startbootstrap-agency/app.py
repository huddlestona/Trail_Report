from __future__ import division
from math import sqrt
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    hike, hike_date = user_data['hike'], user_data['hike_date']
    root_1,root_2= _get_prediction(hike)
    return jsonify({'root_1': root_1, 'root_2': root_2})


def _get_prediction(hike):
    #condition = 'condition|snow'
    #prob,top_text  = Make_Prediction(hike,hike_date,condition)
    #probability = float(prob[:,1])
    #return f"There is a %.2f probability that there is {condition} at {hike} on {hike_date}. <p> Previous reports for similar hike/weather combinations say: <p> {top_text}" %probability
    return "You can {hike}","Here's the snow report."

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
