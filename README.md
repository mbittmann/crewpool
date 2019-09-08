# crewpool

## Setup
`pip install -r requirements.txt`

## Running the Inference Launcher Application

The python launcher module takes a given in-game scenario and prints
the probability that the favorite will cover. There is around 1 sec
of latency for model setup/initilization 

The launcher module takes a set of arguments, described below:
```
-t TIME, --time TIME  (Time elapsed, in seconds, so far in the game)
-s SPREAD, --spread SPREAD    (Spread, relative to visiting team)
-f FAVORITE, --favorite FAVORITE  (Current point total for the favorite)
-u UNDERDOG, --underdog UNDERDOG  (Current point total for the underdog)
```
* Note: Negative numbers are possible for the spread, which may look confusing as it
looks like an extra arg. This happens when the home team is the underdog. 

Examples:  
`python launcher.py -t 2700 -s -3.5 -f 7 -u 14`  
`python launcher.py --time 2700 --spread -3.5 --favorite 7 --underdog 14`

### Example output
```
$ python launcher.py --time 2700 --spread -3.5 --favorite 7 --underdog 3
Using TensorFlow backend.
2019-09-08 09:37:25.581943: I tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
0.5944148
```

## Model Load Initialization Latency


```
%%time
import inference
inference.load_model('model/model.h5')
```

`Wall time: 1.27 s`
