import sys
import logging
import apache_beam as beam

from argparse import ArgumentParser
from datetime import datetime
from os import environ, makedirs
from uuid import uuid4
from utils import schema
from utils.parser import Printer, JSONParser, DateParser

LOG_PATH = environ.get('LOG_PATH', './logs')


def init():
    parser = ArgumentParser()
    parser.add_argument('--input', dest='input', required=True, help='Input file to process.')
    parser.add_argument('--output', dest='output', required=True, help='Output file to write results to.')
    args = parser.parse_args()
    makedirs(args.output, exist_ok=True)
    makedirs(LOG_PATH, exist_ok=True)
    return args


def config():
    app_name, app_version = 'app-processor', '1.0.0'
    date = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    log_file = f'{LOG_PATH}/{app_name}.{app_version}.{date}.log'
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
    return log_file


if __name__ == "__main__":

    args, log_file = init(), config()
    logging.info('Starting job...')
    logging.info(f'Input: "{args.input}"')
    logging.info(f'Output: "{args.output}"')

    with beam.Pipeline(runner="DirectRunner") as pipeline:
        (
            pipeline
            | 'Read Data'         >> beam.io.ReadFromText(args.input)
            | 'Parse JSON'        >> beam.ParDo(JSONParser())
            | 'Remove Invalid'    >> beam.Filter(lambda data: 'id' in data)
            | 'Key/Value Pair'    >> beam.Map(lambda data: (data['id'], data))
            | 'Group by Key'      >> beam.GroupByKey()
            | 'Remove Duplicates' >> beam.Map(lambda data: data[1][0])
            | 'Show IDs'          >> beam.ParDo(Printer())
            | 'Parse Dates'       >> beam.ParDo(DateParser())
            | 'Write Output'      >> beam.io.WriteToParquet(
                f'{args.output}/{uuid4()}',
                schema.jokes(),
                codec='snappy',
                file_name_suffix='.snappy.parquet'
            )
        )

    logging.info(f'Job finished... Log file saved at "{log_file}"')
