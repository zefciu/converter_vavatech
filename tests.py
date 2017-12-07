from converter import CsvFormat
from io import StringIO
from nose.tools import assert_list_equal


def tests_parse_csv():
    """Testujemy prawidłowe parsowanie CSV"""
    plik=  StringIO("""id,imię,nazwisko
1,Anna,Kowalska
2,Zdzisław,Kręcina
3,Daniel,Goszewski""")
    parser = CsvFormat()
    p= parser.parse_file(plik)
    assert_list_equal(p, [
        {'id': '1', 'imię': 'Anna', 'nazwisko': 'Kowalska'},
        {'id': '2', 'imię': 'Zdzisław', 'nazwisko': 'Kręcina'},
        {'id': '3', 'imię': 'Daniel', 'nazwisko': 'Goszewski'},
    ])
