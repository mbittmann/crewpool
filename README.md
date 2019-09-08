# crewpool

## Setup
`pip install -r requirements.txt`

## Running the Inference Launcher Application

The launcher module takes a set of arguments, described below:
```
-t TIME, --time TIME  (Time elapsed, in seconds, so far in the game)
-s SPREAD, --spread SPREAD    (Spread, relative to visiting team)
-f FAVORITE, --favorite FAVORITE  (Current point total for the favorite)
-u UNDERDOG, --underdog UNDERDOG  (Current point total for the underdog)
```
* Note: Negative numbers are possible for the spread, which may look confusing as it
looks like an extra arg. This happens when the home team is the underdog. 

Example: 
`python launcher.py -t 2700 -s -3 -f 7 -u 14`

OR

`python launcher.py --time 2700 --spread -3 --favorite 7 --underdog 14`

## Model Load Initialization Latency


```
%%time
import inference
inference.load_model('model/model.h5')
```

`Wall time: 1.27 s`
