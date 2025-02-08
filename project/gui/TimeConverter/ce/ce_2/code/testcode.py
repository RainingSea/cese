import unittest
from TimeConverter import TimeConverter

class TestTimeConverter(unittest.TestCase):

    def test_convert_time_between_time_zones(self):
        # Test case 1: Convert time from UTC to EST
        converter = TimeConverter("12:00 PM", "UTC", "America/New_York", "%I:%M %p")
        result = converter.convert_time()
        self.assertEqual(result, "07:00 AM")

        # Test case 2: Convert time from PST to GMT
        converter = TimeConverter("03:00 PM", "America/Los_Angeles", "GMT", "%I:%M %p")
        result = converter.convert_time()
        self.assertEqual(result, "11:00 PM")

    def test_convert_time_between_formats(self):
        # Test case 1: Convert 24-hour format to 12-hour format
        converter = TimeConverter("15:30", "UTC", "UTC", "%H:%M")
        result = converter.convert_time()
        self.assertEqual(result, "03:30 PM")

        # Test case 2: Convert 12-hour format to 24-hour format
        converter = TimeConverter("09:45 AM", "UTC", "UTC", "%I:%M %p")
        result = converter.convert_time()
        self.assertEqual(result, "09:45")

if __name__ == '__main__':
    unittest.main()
