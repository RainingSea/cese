import unittest
import os
from time_converter import TimeConverter

class TestTimeConverter(unittest.TestCase):

    def setUp(self):
        self.time_converter = TimeConverter()
        self.history_file = "conversion_history.txt"
        # Clear the history file before each test
        if os.path.exists(self.history_file):
            os.remove(self.history_file)

    def test_convert_time_between_time_zones(self):
        # Functionality 1: Convert Time Between Different Time Zones
        # Test case 1
        converted_time_1 = self.time_converter.convert_time("12:00 PM", "UTC", "EST", "12-hour")
        self.assertEqual(converted_time_1, "07:00 AM")

        # Test case 2
        converted_time_2 = self.time_converter.convert_time("15:00", "PST", "GMT", "12-hour")
        self.assertEqual(converted_time_2, "11:00 PM")

    def test_convert_time_between_formats(self):
        # Functionality 2: Convert Time Between Different Formats
        # Test case 1
        converted_time_3 = self.time_converter.convert_time("15:30", "UTC", "UTC", "12-hour")
        self.assertEqual(converted_time_3, "03:30 PM")

        # Test case 2
        converted_time_4 = self.time_converter.convert_time("09:45 AM", "UTC", "UTC", "24-hour")
        self.assertEqual(converted_time_4, "09:45")

    def test_save_conversion(self):
        # Test saving conversion history
        self.time_converter.save_conversion("12:00 PM", "UTC", "EST", "07:00 AM", "12-hour")
        history = self.time_converter.load_history()
        self.assertEqual(len(history), 1)
        self.assertIn("12:00 PM, UTC, EST, 07:00 AM, 12-hour", history[0])

    def test_load_history(self):
        # Test loading history when file does not exist
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
        history = self.time_converter.load_history()
        self.assertEqual(history, [])

    def test_clear_history(self):
        # Test clearing history
        self.time_converter.save_conversion("12:00 PM", "UTC", "EST", "07:00 AM", "12-hour")
        self.time_converter.clear_history()
        history = self.time_converter.load_history()
        self.assertEqual(history, [])

if __name__ == '__main__':
    unittest.main()
