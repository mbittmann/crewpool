import keras.models

def load_model(model_path):
    model = keras.models.load_model(model_path)
    return model