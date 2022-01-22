import unittest
from pii_data import read_data


class DataTestCases(unittest.TestCase):
    def test_read_data(self):
        expected_data = ['Aggie Pride Worldwide',
                         'Aggies Do',
                         'Aggie Strong!',
                         'Go Aggies',
                         'Aggies #1',
                         'Aggie Pride',
                         'Aggies All The Way']

        data = read_data('sample_data.txt')

        self.assertEqual(data, expected_data)


if __name__ == '__main__':
    unittest.main()
