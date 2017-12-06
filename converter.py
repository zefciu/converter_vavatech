import argparse
import csv
import json


# 1. Wczytać dane z csv
# 2. Przekonwertować dane na listę
# 3. Zapisać w formacie JSON

class JsonFormat:

    def __init__(self, **kwars):
        pass

    def parse(self, fileName):
        with open(fileName, 'r') as fRead:
            return json.load(fRead)

    def output(self, lTab, fileName):
        with open(fileName, 'w') as fWrite:
            json.dump(lTab, fWrite)


class CsvFormat:

    def __init__(self, **kwars):
        pass

    def parse(self, filename):
        with open(filename, 'r') as fRead:
            reader = csv.DictReader(fRead)
            return list(reader)

    def output(self, lTab, filename):
        with open(filename, 'w') as fWrite:
            writer = csv.DictWriter(fWrite, fieldnames=lTab[0].keys())
            writer.writeheader()
            writer.writerows(lTab)


FORMATS = {
    'json': JsonFormat,
    'csv': CsvFormat,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Converts between dataformats'
    )
    parser.add_argument('infile')
    parser.add_argument('outfile')
    parser.add_argument(
        '-i', '--input-format',
        required=True,
        choices=FORMATS.keys()
    )
    parser.add_argument(
        '-o', '--output-format',
        required=True,
        choices=FORMATS.keys()
    )
    args = parser.parse_args()
    inputFormat = args.input_format
    outputFormat = args.output_format
    
    data_parser = FORMATS[inputFormat]()
    formatter = FORMATS[outputFormat]()
    parsedValue = data_parser.parse(args.infile)
    if len(parsedValue) == 0:
        parser.error('Conversion of empty data not supported')
    formatter.output(parsedValue, args.outfile)
