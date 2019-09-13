from flask import Flask, request, g
from werkzeug.exceptions import BadRequest
import logging
import logging.handlers as handlers

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

def get_model():
    if 'model' not in g:
        g.model = inference.load_model(MODEL_PATH)
    return g.model

def get_scalar():
    if 'scaler' not in g:
        g.scaler = inference.load_scaler(SCALER_PATH)
    return g.scaler

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

    model = get_model()
    scaler = get_scalar()
    pred = inference.run_inference(model, scaler, time_sec, spread, 
                                   favorite_points, underdog_points)

    return {"cover_probability": float(pred)}
    

if __name__ == "__main__":
    app.run()