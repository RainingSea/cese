import unittest
import os
from main import TimeConverter, HistoryManager

class TestTimeConverter(unittest.TestCase):

    def setUp(self):
        # Setup for the tests
        self.history_manager = HistoryManager()
        self.history_manager.clear_history()  # Ensure history is clear before each test

    def test_convert_time_between_different_time_zones(self):
        # Functionality 1: Convert Time Between Different Time Zones
        # Test case 1
        converter_1 = TimeConverter("2023-10-01 12:00", "UTC", "America/New_York", "12-hour")
        converted_time_1 = converter_1.convert_time()
        self.assertEqual(converted_time_1, "2023-10-01 07:00 PM")

        # Test case 2
        converter_2 = TimeConverter("2023-10-01 15:00", "America/Los_Angeles", "GMT", "24-hour")
        converted_time_2 = converter_2.convert_time()
        self.assertEqual(converted_time_2, "2023-10-01 22:00")

    def test_convert_time_between_different_formats(self):
        # Functionality 2: Convert Time Between Different Formats
        # Test case 1
        converter_3 = TimeConverter("2023-10-01 15:30", "UTC", "America/New_York", "12-hour")
        converted_time_3 = converter_3.convert_time()
        self.assertEqual(converted_time_3, "2023-10-01 03:30 PM")

        # Test case 2
        converter_4 = TimeConverter("2023-10-01 09:45 AM", "America/New_York", "UTC", "24-hour")
        converted_time_4 = converter_4.convert_time()
        self.assertEqual(converted_time_4, "2023-10-01 09:45")

    def test_save_history(self):
        # Test saving history
        converter = TimeConverter("2023-10-01 12:00", "UTC", "America/New_York", "12-hour")
        converter.convert_time()  # Perform conversion to save history
        converter.save_history()

        # Check if history is saved correctly
        with open('conversion_history.txt', 'r') as file:
            lines = file.readlines()
            self.assertIn("2023-10-01 12:00,2023-10-01 07:00 PM,UTC,America/New_York,12-hour\n", lines)

    def test_clear_history(self):
        # Test clearing history
        self.history_manager.save_history(["2023-10-01 12:00,2023-10-01 07:00 PM,UTC,America/New_York,12-hour"])
        self.history_manager.clear_history()

        # Check if history is cleared
        self.assertEqual(self.history_manager.history, [])
        with open('conversion_history.txt', 'r') as file:
            lines = file.readlines()
            self.assertEqual(lines, [])

if __name__ == '__main__':
    unittest.main()
