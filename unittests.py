import unittest
import calendar
from util import getWeekendDate
from parameterized import parameterized


class TestWeekendDate(unittest.TestCase):
    
    @parameterized.expand([
        (2022, 9, [2, 3, 9, 10, 16, 17, 23, 24]),
        (2022, 10, [0, 1, 7, 8, 14, 15, 21, 22, 28, 29]),
        (2022, 11, [4, 5, 11, 12, 18, 19, 25, 26]),
        (2022, 12, [2, 3, 9, 10, 16, 17, 23, 24, 30]),
        (2023, 1, [0, 6, 7, 13, 14, 20, 21, 27, 28]),
        (2023, 2, [3, 4, 10, 11, 17, 18, 24, 25]),
        (2023, 3, [3, 4, 10, 11, 17, 18, 24, 25]),
        (2023, 4, [0, 1, 7, 8, 14, 15, 21, 22, 28, 29]),
        (2023, 5, [5, 6, 12, 13, 19, 20, 26, 27]),
        (2023, 6, [2, 3, 9, 10, 16, 17, 23, 24]),
        (2023, 7, [0, 1, 7, 8, 14, 15, 21, 22, 28, 29]),
        (2023, 8, [4, 5, 11, 12, 18, 19, 25, 26]),
        (2023, 9, [1, 2, 8, 9, 15, 16, 22, 23, 29]),
        (2023, 10, [0, 6, 7, 13, 14, 20, 21, 27, 28]),
        (2023, 11, [3, 4, 10, 11, 17, 18, 24, 25])
       ])
    def testGetWeekendDate(self, year, month, expected):
        weekend_dates = getWeekendDate(year, month)
        self.assertEqual(weekend_dates, expected)

if __name__ == '__main__':
    unittest.main()