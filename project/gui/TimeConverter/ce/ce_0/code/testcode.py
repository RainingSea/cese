import unittest
from time_converter import TimeConverter

class TestTimeConverter(unittest.TestCase):

    def setUp(self):
        self.converter = TimeConverter()

    def test_convert_time_between_time_zones(self):
        # Test case 1: Convert from UTC to EST
        input_time = "2023-10-10 12:00:00"
        source_tz = "UTC"
        target_tz = "America/New_York"
        format_type = "%Y-%m-%d %H:%M:%S"
        expected_output = "2023-10-10 07:00:00"
        result = self.converter.convert_time(input_time, source_tz, target_tz, format_type)
        self.assertEqual(result, expected_output)

        # Test case 2: Convert from PST to GMT
        input_time = "2023-10-10 15:00:00"
        source_tz = "America/Los_Angeles"
        target_tz = "Europe/London"
        format_type = "%Y-%m-%d %H:%M:%S"
        expected_output = "2023-10-10 23:00:00"
        result = self.converter.convert_time(input_time, source_tz, target_tz, format_type)
        self.assertEqual(result, expected_output)

    def test_convert_time_between_formats(self):
        # Test case 1: Convert from 24-hour to 12-hour format
        input_time = "2023-10-10 15:30:00"
        source_tz = "UTC"
        target_tz = "UTC"
        format_type = "%Y-%m-%d %H:%M:%S"
        expected_output = "2023-10-10 03:30:00 PM"
        result = self.converter.convert_time(input_time, source_tz, target_tz, format_type)
        self.assertEqual(result, expected_output)

        # Test case 2: Convert from 12-hour to 24-hour format
        input_time = "2023-10-10 09:45:00"
        source_tz = "UTC"
        target_tz = "UTC"
        format_type = "%Y-%m-%d %H:%M:%S"
        expected_output = "2023-10-10 09:45:00"
        result = self.converter.convert_time(input_time, source_tz, target_tz, format_type)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
