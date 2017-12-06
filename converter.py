import csv
import json

IN_FILE = 'MOCK_DATA.csv'
OUT_FILE = 'MOCK_DATA.json'

# 1. Wczytać dane z csv
# 2. Przekonwertować dane na listę
# 3. Zapisać w formacie JSON

values = []

with open (IN_FILE) as f:
    reader = csv.DictReader(f)
    for row in reader:
        values.append(row) 


with open (OUT_FILE,'w') as o:
    json.dump(values, o)


