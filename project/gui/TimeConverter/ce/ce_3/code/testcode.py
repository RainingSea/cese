import unittest
from ui import UI
from time_converter import TimeConverter

class TestTimeConverter(unittest.TestCase):

    def setUp(self):
        self.ui = UI()
        self.ui.root.update()  # Ensure the UI is fully loaded

    def test_convert_time_between_different_time_zones(self):
        # Test case 1: UTC to EST
        self.ui.input_time_entry.insert(0, "2023-01-01 12:00")
        self.ui.source_timezone_entry.insert(0, "UTC")
        self.ui.target_timezone_entry.insert(0, "America/New_York")
        self.ui.time_format_entry.insert(0, "12-hour")
        self.ui.perform_conversion()
        self.assertEqual(self.ui.result_label.cget("text"), "Converted Time: 2023-01-01 07:00 AM")

        # Clear entries for the next test case
        self.ui.input_time_entry.delete(0, 'end')
        self.ui.source_timezone_entry.delete(0, 'end')
        self.ui.target_timezone_entry.delete(0, 'end')
        self.ui.time_format_entry.delete(0, 'end')

        # Test case 2: PST to GMT
        self.ui.input_time_entry.insert(0, "2023-01-01 15:00")
        self.ui.source_timezone_entry.insert(0, "America/Los_Angeles")
        self.ui.target_timezone_entry.insert(0, "Europe/London")
        self.ui.time_format_entry.insert(0, "24-hour")
        self.ui.perform_conversion()
        self.assertEqual(self.ui.result_label.cget("text"), "Converted Time: 2023-01-02 23:00")

    def test_convert_time_between_different_formats(self):
        # Test case 1: 24-hour to 12-hour
        self.ui.input_time_entry.insert(0, "2023-01-01 15:30")
        self.ui.source_timezone_entry.insert(0, "UTC")
        self.ui.target_timezone_entry.insert(0, "UTC")
        self.ui.time_format_entry.insert(0, "12-hour")
        self.ui.perform_conversion()
        self.assertEqual(self.ui.result_label.cget("text"), "Converted Time: 2023-01-01 03:30 PM")

        # Clear entries for the next test case
        self.ui.input_time_entry.delete(0, 'end')
        self.ui.source_timezone_entry.delete(0, 'end')
        self.ui.target_timezone_entry.delete(0, 'end')
        self.ui.time_format_entry.delete(0, 'end')

        # Test case 2: 12-hour to 24-hour
        self.ui.input_time_entry.insert(0, "2023-01-01 09:45 AM")
        self.ui.source_timezone_entry.insert(0, "UTC")
        self.ui.target_timezone_entry.insert(0, "UTC")
        self.ui.time_format_entry.insert(0, "24-hour")
        self.ui.perform_conversion()
        self.assertEqual(self.ui.result_label.cget("text"), "Converted Time: 2023-01-01 09:45")

if __name__ == '__main__':
    unittest.main()
