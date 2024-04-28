#!/bin/bash

# start environment
poetry shell

# install dependencies
poetry install

# migrate
python3 manage.py migrate

# run custom command to seed database
python3 manage.py seed_parking_rates

# run the server
python3 manage.py runserver 5000
