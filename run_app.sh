#!/bin/bash

# start environment
poetry shell

# install dependencies
poetry install

# migrate
python manage.py migrate

# run custom command
python manage.py seed_parking_rates


python manage.py runserver 5000
