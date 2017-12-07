import argparse
import csv
import json
import pickle
import sqlite3


class OpenFileFormat:
    def parse(self, filename):
        if self.binary:
            mode = 'rb'
        else:
            mode = 'r'
        with open(filename, mode) as f:
            return self.parse_file(f)

    def output(self, data, filename):
        if self.binary:
            mode = 'wb'
        else:
            mode = 'w'
        with open(filename, mode) as f:
            return self.output_file(data, f)


class DumpLoadFormat(OpenFileFormat):
    def parse_file(self, f):
        return self.mod.load(f)

    def output_file(self, data, f):
        self.mod.dump(data, f)


class SqliteFormat:
    def parse(self, f):
        raise NotImplementedError

    def output(self, data, f):
        c = sqlite3.connect(f)
        colName=data[0].keys()
        colNames=",".join(colName)
        cur = c.cursor()
        cur.execute('DROP TABLE IF EXISTS data')
        cur.execute('CREATE TABLE data (' + colNames +');')
        exl_marks = ",".join(['?']*len(colName))
        for i in data:
            stmt = (
                'INSERT INTO data (' +
                colNames +
                ') VALUES (' +
                exl_marks +
                ');'
            )
            cur.execute(stmt, tuple(i.values()))
        c.commit()
        c.close()


class PickleFormat(DumpLoadFormat):
    mod = pickle
    binary = True


class JsonFormat(DumpLoadFormat):
    mod = json
    binary = False


class CsvFormat(OpenFileFormat):
    binary = False

    def parse_file(self, f):
        reader = csv.DictReader(f)
        return list(reader)

    def output_file(self, lTab, f):
        writer = csv.DictWriter(f, fieldnames=lTab[0].keys())
        writer.writeheader()
        writer.writerows(lTab)


FORMATS = {
    'json': JsonFormat,
    'csv': CsvFormat,
    'pickle': PickleFormat,
    'sqlite': SqliteFormat,
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
