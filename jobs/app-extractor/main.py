import requests
import logging
import json

from os import environ, makedirs
from datetime import datetime
from time import sleep
from uuid import uuid4


API_URL    = environ.get('API_URL', 'https://api.chucknorris.io/jokes/random')
LAKE_PATH  = environ.get('LAKE_PATH', './output/jokes')
LOG_PATH   = environ.get('LOG_PATH', './logs')
HOW_MANY   = int(environ.get('HOW_MANY', '10'))
SLEEP_TIME = int(environ.get('SLEEP_TIME', '1'))


def init():
    makedirs(LOG_PATH, exist_ok=True)
    makedirs(LAKE_PATH, exist_ok=True)
    logging.basicConfig(
        filename=log_file(),
        filemode='a',
        format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG
    )


def log_file():
    app_name, app_version = 'app-extractor', '1.0.0'
    date = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f'{LOG_PATH}/{app_name}.{app_version}.{date}.log'


def save(data):
    if data:
        file_name = f'{LAKE_PATH}/{uuid4()}.json'
        logging.debug(f'Writing file "{file_name}"')
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile)


def request():
    data = requests.get(API_URL).json()
    if data:
        data['persisted_at'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    logging.debug(f'Response Data: {data}')
    return data


if __name__ == '__main__':

    init()
    logging.info(f'Starting {HOW_MANY} executions...')

    for i in range(HOW_MANY):
        count = f'({i+1}/{HOW_MANY})'

        logging.info(f'{count} Requesting data...')
        data = request()

        logging.info(f'{count} Saving data...')
        save(data)

        logging.info(f'{count} Done!')
        sleep(SLEEP_TIME)
