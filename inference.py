# Ignore tensorflow future deprecation warnings
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

import keras.models

def load_model(model_path):
    model = keras.models.load_model(model_path)
    return model