# crewpool
This repository contains a set of analytics for crewpool. 

**This repo contains code used for personal and non-commercial use by a group of NFL fans and tech hobbyests.**

## Setup
`pip install -r requirements.txt`

## Running in dev
`FLASK_DEBUG=1 python server.py`

## Running the Data Server Application

The Data Server is a simple python/Flask RESTful web server. 

The Data Server uses a virtuel environment on the server to manage all python
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


