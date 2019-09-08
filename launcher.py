import inference
import argparse

MODEL_PATH = 'model/model.h5'
SCALER_PATH = 'model/scaler.pkl'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", help="Time elapsed, in seconds, so far in the game", 
                        required=True, type=int)
    parser.add_argument("-s", "--spread", help="Spread, relative to visiting team", 
                        required=True, type=float)
    parser.add_argument("-f", "--favorite", help="Current point total for the favorite", 
                        required=True, type=int)
    parser.add_argument("-u", "--underdog", help="Current point total for the underdog", 
                        required=True, type=int)
    args = parser.parse_args()

    
    time_sec = args.time
    spread = args.spread
    favorite_points = args.favorite
    underdog_points = args.underdog

    assert time_sec > 0, "Time must be a positive integer"
    assert favorite_points > 0, "Favorite points must be a positive integer"
    assert favorite_points > 0, "Underdog points must be a positive integer"

    model = inference.load_model(MODEL_PATH)
    scaler = inference.load_scaler(SCALER_PATH)

    pred = inference.run_inference(model, scaler, time_sec, spread, 
                                   favorite_points, underdog_points)

    print(pred)


if __name__ == "__main__":
    main()