from flask import Flask, request
from werkzeug.exceptions import BadRequest
import logging
import logging.handlers as handlers
import time
import tensorflow as tf
import keras
import joblib

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
def get_game_data(year, phase, week):

    if phase.upper() not in {"PRE", "REG", "POST"}:
        raise BadRequest('Phase must be one of PRE, REG, POST')
    return year


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