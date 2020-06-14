import json
import logging
import apache_beam as beam
from datetime import datetime


class Printer(beam.DoFn):
    def process(self, element):
        logging.info(f'Record ID: {element["id"]}')
        return [element]


class JSONParser(beam.DoFn):
    def process(self, element):
        try:
            return [json.loads(element)]
        except Exception as ex:
            return None


class DateParser(beam.DoFn):

    def process(self, element):
        element['created_at'] = self.parse(element, 'created_at', '%Y-%d-%m %H:%M:%S.%f')
        element['updated_at'] = self.parse(element, 'updated_at', '%Y-%d-%m %H:%M:%S.%f')
        element['persisted_at'] = self.parse(element, 'persisted_at', '%Y-%m-%d %H:%M:%S')
        return [element]

    def parse(self, element, field, pattern):
        date = None
        try:
            if field in element:
                date = datetime.strptime(element[field], pattern).timestamp()
            else:
                logging.warning(f'Field "{field}" not found!')
        except:
            logging.warning(f'Error while parsing date "{element[field]}" using "{pattern}" pattern.')
        return date

