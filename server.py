from flask import Flask, request
from werkzeug.exceptions import BadRequest, HTTPException
import logging
import logging.handlers as handlers
import time
import tensorflow as tf
import keras
import joblib

import nfl_api
import espn_api
import inference 

"""
Example Usage:
curl -H "Content-Type: application/json" \
    -X POST localhost:5000/game/inference \
    -d '{"time_sec": 2000, "hspread": -5, "favorite_points": 17, "underdog_points": 15}'
"""

app = Flask(__name__)

# Setup logging
app.logger.setLevel(logging.DEBUG)
logHandler = handlers.RotatingFileHandler('logs/app.log', maxBytes=1000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logHandler.setFormatter(formatter)
app.logger.addHandler(logHandler)

MODEL_PATH = 'model/model.h5'
SCALER_PATH = 'model/scaler.pkl'

# load the model the model and scaler globally on startup
global graph  # Allow the graph to be accessed within the app context
graph = tf.get_default_graph()
model =inference.load_model(MODEL_PATH)
scaler = inference.load_scaler(SCALER_PATH)

@app.route("/games/<year>/<phase>/<week>")
def get_game_data_by_week(year, phase, week):
    app.logger.debug("Starting request for game data for {}:{}{}".format(year, phase, week))
    if phase.upper() not in {"PRE", "REG", "POST"}:
        raise BadRequest('Phase must be one of PRE, REG, POST')
    try:
        game_data = nfl_api.get_game_data(year, phase, week)
    except Exception as e:
        app.logger.error(e)
        raise HTTPException("Error collecting game data")

    return_val = dict()
    return_val['year'] = year
    return_val['phase'] = phase
    return_val['week'] = week
    return_val['games'] = game_data
    return return_val

@app.route("/games/")
def get_game_data():
    app.logger.debug("Starting request for current game data")

    try:
        game_data = espn_api.get_game_data()
    except Exception as e:
        app.logger.error(e)
        raise HTTPException("Error collecting game data")

    return_val = dict()
    return_val['games'] = game_data
    return return_val


@app.route("/game/inference", methods=['POST'])
def run_inference():
    try:
        input = request.get_json()
    except BadRequest as e:
        app.logger.error(e)
        app.logger.error("Raw request body is: {}".format(request.get_data()))
        return e.description

    app.logger.debug("JSON request body is: {}".format(input))
    time_sec = int(input["time_sec"])
    hspread = input["hspread"]  # The database stores spread relative to the home team
    spread = -1*hspread  # The model uses spread relative to the visiting team
    favorite_points = int(input["favorite_points"])
    underdog_points = int(input["underdog_points"])

    start = time.time()
    with graph.as_default():
        pred = inference.run_inference(model, scaler, time_sec, spread, 
                                       favorite_points, underdog_points)
    end = time.time()
    app.logger.debug("Finished in {} secs".format(end - start))
    return {"cover_probability": float(pred)}
    

if __name__ == "__main__":
    app.run()