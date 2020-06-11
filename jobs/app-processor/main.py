import apache_beam as beam
import re
import json
import pyarrow

# TODO: Create Docker File
# TODO: Remove this and use ArgParser
inputs_pattern = 'data/*.json'
outputs_prefix = 'output/part'

# TODO: Create Utils Parser File
class Printer(beam.DoFn):
    def process(self, element):
        print(f'Record ID: {element["id"]}')
        return [element]


class JSONParser(beam.DoFn):
    def process(self, element):
        try:
            return [json.loads(element)]
        except Exception as ex:
            return None


# TODO: Update Parser
class DateParser(beam.DoFn):
    
    def process(self, element):
        element['x'] = self.parse(element['x'], 'pattern')
    
    def parse(self, date_str, pattern):
        return None


def schema():
    # TODO: Update Schema
    return pyarrow.schema([
        ('id', pyarrow.string()),
        ('value', pyarrow.string())
    ])


if __name__ == "__main__":
    # Running locally in the DirectRunner.
    with beam.Pipeline() as pipeline:
        (
            pipeline
            | 'Read Data'         >> beam.io.ReadFromText(pipeline.options.)
            | 'Parse JSON'        >> beam.ParDo(JSONParser())
            | 'Remove Invalid'    >> beam.Filter(lambda data: 'id' in data)
            | 'Key/Value Pair'    >> beam.Map(lambda data: (data['id'], data))
            | 'Group by Key'      >> beam.GroupByKey()
            | 'Remove Duplicates' >> beam.Map(lambda data: data[1][0])
            | 'Parse JSON'        >> beam.ParDo(JSONParser())
            | 'Show IDs'          >> beam.ParDo(Printer())
            | 'Write Output'      >> beam.io.WriteToParquet(
                outputs_prefix, schema(), codec='snappy', file_name_suffix='.snappy.parquet'
            )
        )
        # TODO: ArgParser 4 input file pattern.
        # TODO: ArgParser 4 output dir.
        # TODO: Random Output Name.