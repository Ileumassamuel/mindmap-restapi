#!/bin/sh

# bootstrap the virtual env if necessary
if [ -f "venv/bin/activate" ]
then
    echo virtual env already created
else
    python -m venv venv
fi

source venv/bin/activate

# Just install dependencies by default to pick up any changes
pip install -r requirements.txt

export FLASK_ENV="${FLASK_ENV:=development}"
export FLASK_APP="index.py"

flask run -h 0.0.0.0 -p 3000
