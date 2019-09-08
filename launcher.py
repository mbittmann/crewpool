import inference
import argparse

MODEL_PATH = 'model/model.h5'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", help="Time elapsed, in seconds, so far in the game", 
                        required=True, type=int)
    parser.add_argument("-s", "--spread", help="Spread, relative to visiting team", 
                        required=True, type=int)
    parser.add_argument("-f", "--favorite", help="Current point total for the favorite", 
                        required=True, type=int)
    parser.add_argument("-u", "--underdog", help="Current point total for the underdog", 
                        required=True, type=int)
    args = parser.parse_args()

    
    time_sec = args.time
    spread = args.spread
    favorite_points = args.favorite
    underdog_points = args.underdog

    model = inference.load_model(MODEL_PATH)

if __name__ == "__main__":
    main()