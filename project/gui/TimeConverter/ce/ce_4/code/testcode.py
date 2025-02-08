import unittest
from datetime import datetime
import pytz
from main import TimeConverter

class TestTimeConverter(unittest.TestCase):

    def setUp(self):
        # This method will be called before each test
        self.time_format = "%Y-%m-%d %I:%M %p"

    def test_convert_time_between_time_zones(self):
        # Test case 1: Convert time from UTC to EST
        converter = TimeConverter("12:00 PM", "UTC", "America/New_York", "%I:%M %p")
        converted_time = converter.convert_time()
        expected_time = "07:00 AM"
        self.assertEqual(converted_time, expected_time)

        # Test case 2: Convert time from PST to GMT
        converter = TimeConverter("03:00 PM", "America/Los_Angeles", "GMT", "%I:%M %p")
        converted_time = converter.convert_time()
        expected_time = "11:00 PM"
        self.assertEqual(converted_time, expected_time)

    def test_convert_time_between_formats(self):
        # Test case 1: Convert 24-hour format to 12-hour format
        converter = TimeConverter("15:30", "UTC", "UTC", "%H:%M")
        converted_time = converter.convert_time()
        expected_time = "03:30 PM"
        self.assertEqual(converted_time, expected_time)

        # Test case 2: Convert 12-hour format to 24-hour format
        converter = TimeConverter("09:45 AM", "UTC", "UTC", "%I:%M %p")
        converted_time = converter.convert_time()
        expected_time = "09:45"
        self.assertEqual(converted_time, expected_time)

if __name__ == '__main__':
    unittest.main()
