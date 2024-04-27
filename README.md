

# Parking Rates API


## Table of Contents
- [Installation](#installation)
- [Endpoints](#endpoints)
- [Notes](#notes)


## Installation

Setup requirements:
- Python 3.12
- Poetry 1.8.2


##### To easily setup for the first time:
```bash
chmod +x run_app.sh
./run_app.sh
```


##### Then feel free to start the server with the following:
```python
./manage.py runserver {PORT number}
```
==Note: This application is configured to run on port 5000 by default; however you may already have a process running on that port. In which case, please enter in 5000 after runserver==


## Endpoints

#### GET /api/rates/
- Description: Retrieve a list of all rates.
- Parameters: None
- Response:
```json
[
    {
        "days": "mon,tues,thurs",
        "times": "0900-2100",
        "tz": "America/Chicago",
        "price": 1500
    },
    {
        "days": "fri,sat,sun",
        "times": "0900-2100",
        "tz": "America/Chicago",
        "price": 2000
    }
]
```


#### PUT /api/rates/
- Description: Updates existing parking rate instance.
- Parameters:
    - `days` (string): Shorthand days of the week, separated by a comma, and without any spaces
    - `times` (string): Local time range; the first number being the start time and the number following the `-` is the end time
        - Must be in 0000-0000 format
        - The start time must occur before the end time
    - `tz` (string): Name of timezone the `times` field is in
        - `tz` must match a timezone listed [here](https://gist.github.com/JellyWX/913dfc8b63d45192ad6cb54c829324ee)
    - `price` (integer): New price to update rate with

- Request Body:
    ```json
    {
        "days": "mon,wed,sat",
        "times": "0200-0600",
        "tz": "America/New_York",
        "price": 2500
    }
    ```

- Response: Returns new price
    ```json
    {
        "price": 2500
    }
    ```
    - If the given rate does not exist, you will receive the following message:
    `"No instance found to update"`
    - If the given rate has the same data as the found rate, then there is nothing to update:
    `"Given data matches perfectly - nothing to update`

#### GET /api/price/
- Description: Request the price for a given ISO-8601 time range.
- Parameters:
    - `start` (string): Start datetime in ISO-8601 format
    - `end` (string): End datetime in ISO-8601 format
- Query Parameters:
    `?start=2015-07-01T07:00:00-05:00&end=2015-07-01T12:00:00-05:00`
- Response: If found, returns the price 
    - If there was nothing found in the given time range or the time range spans over a day, the response will be:
    `"unavailable"`
