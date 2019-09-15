# crewpool
This repository contains a set of analytics for crewpool. 

## In-Game "Cover Probability" Service Overview
The "cover probability" service predicts the probability, given a set of 
in-game attributes, that the favorite will cover the spread. Before a game
starts, the probability that the favorite will cover the spread is pretty 
close to 50%. However, once the clock starts to tick and teams start to score
points (or not), the odds that the favorite will cover may be above or 
below 50%. For example, suppose the spread is 5.5, but the underdog is 
up by 3 points with 10 minutes left in the fourth quarter. In this case,
the favorite needs to score 8.5 points to cover, meaning it is a 2-score
game. If the favorite scores a touchdown, now it only needs a field goal 
(or safety) to cover the spread, so the odds will get a little better, 
but the underdog still has the advantage. In theory, this probability 
changes for every second that ticks off the clock and for every scoring 
event, and the cover probability service provides this for all in
game scenarios.

To create this service, we created a "deep learning" artificial neural network.
Deep learning is common machine learning technique used today for computer 
vision, natural laungage processing, and algorithmic trading. 

We trained the neural network on a dataset of over 500,000 historical NFL 
plays. Each "play" contains the game clock and the current points
for each team. We combine each "play" with game-level data like the spread
the final score. We can derive a field as to whether the favorite covered 
the spread. This derived field serves as the "target variable" used
to train a classification model with the neural network. 

Once the neural network is trained, we can evaluate any in-game situation
and compute a probability that the favorite will cover the spread. This
is called performing "inference" on the model. With this service,
we can display, in real time, the probability for each game that 
each crewpool user will "win" that game. 

The probability for each game is:
- For games that are completed, the win probabilty is already known, so it will
be 1 or 0
- For games that are ongoing, the win probability is derived by the deep learning
model
- For games that haven't started, the win probability is 50%


## Setup
`pip install -r requirements.txt`

## Running the Inference Server Application

The Inference Server is a simple python/Flask RESTful web server. It has one
end point that accepts an in-game scenario and returns the probability that 
the favorite will cover the spread. 

The Inference Server uses a virtuel environment on the server to manage all python
dependencies. To activate the virtual environment, navigate to 
`APP_HOME/crewpool/` and run 
```
source env/bin/activate
```

In production, the server runs under gunicorn in daemon mode. To start the server, 
run: 
```
gunicorn --worker-class gevent --workers 1 --timeout 300 --log-file logs/gunicorn.log --bind 0.0.0.0:5000 server:app --daemon
```

Logs can be found in `APP_HOME/logs/`

## Querying the Inference Server Application

The REST server expects a POST request with a JSON body at the endpoint 
`HOST:PORT/game/inference` 

The fields for the JSON body are:
- `time_sec`: Time elapsed, in seconds, so far in the game
- `hspread`: Spread, relative to home team. (Note: the model 
uses spread relative to the visiting team, but the upstream 
database stores it relative to the home team. So the server accepts
hspread and converts it to vspread) 
- `favorite_points`: Current point total for the favorite
- `underdog_points`: Current point total for the underdog

Example REST Usage:
```
curl -H "Content-Type: application/json" \
    -X POST localhost:5000/game/inference \
    -d '{"time_sec": 2000, "hspread": -5, "favorite_points": 17, "underdog_points": 15}'
```

Returns: 
```
{"cover_probability":0.4222043752670288}
```

## Running the Inference Command Line Application

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
