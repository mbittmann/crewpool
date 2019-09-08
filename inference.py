# Ignore tensorflow future deprecation warnings
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

import keras.models
import joblib
import pandas as pd


def load_model(model_path):
    model = keras.models.load_model(model_path)
    return model

def load_scaler(scaler_path):
    scaler = joblib.load(scaler_path) 
    return scaler

def run_inference(model, scaler, time_sec, spread, favorite_points, underdog_points):
    payload = {}
    payload['time_elapsed_sec'] =  time_sec
    payload['spread'] = spread
    payload['home_dog'] = int(spread < 0)
    payload['current_points_favorite'] = favorite_points
    payload['current_points_underdog'] = underdog_points
    df = pd.DataFrame.from_dict([payload])

    scaled = scaler.transform(df)
    pred = model.predict(scaled)
    return pred[0][0]