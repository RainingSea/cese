import unittest
import subprocess
import time
from tkinter import Tk
from main import Main

class TestTimeConverter(unittest.TestCase):

    def setUp(self):
        # Start the Time Converter application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the application to start

    def tearDown(self):
        # Terminate the application after tests
        self.process.terminate()
        self.process.wait()

    def test_convert_time_between_time_zones(self):
        # Functionality 1: Convert Time Between Different Time Zones
        # Test case 1
        self._set_time_zone_and_convert("UTC", "12:00 PM", "US/Eastern", "7:00 AM")
        # Test case 2
        self._set_time_zone_and_convert("PST", "3:00 PM", "GMT", "11:00 PM")

    def test_convert_time_between_formats(self):
        # Functionality 2: Convert Time Between Different Formats
        # Test case 1
        self._set_time_and_format_and_convert("15:30", "12-hour", "3:30 PM")
        # Test case 2
        self._set_time_and_format_and_convert("9:45 AM", "24-hour", "09:45")

    def _set_time_zone_and_convert(self, source_tz, source_time, target_tz, expected_output):
        # Helper function to set time zone and convert
        root = Tk()
        app = Main()
        app.source_tz.set(source_tz)
        app.time_entry.insert(0, source_time)
        app.target_tz.set(target_tz)
        app.convert_time()
        time.sleep(1)  # Wait for conversion to complete
        converted_time = app.converted_time_display.cget("text")
        self.assertEqual(converted_time, expected_output)

    def _set_time_and_format_and_convert(self, time_input, format_selection, expected_output):
        # Helper function to set time and format and convert
        root = Tk()
        app = Main()
        app.time_entry.insert(0, time_input)
        app.format_var.set(format_selection)
        app.convert_time()
        time.sleep(1)  # Wait for conversion to complete
        converted_time = app.converted_time_display.cget("text")
        self.assertEqual(converted_time, expected_output)

if __name__ == '__main__':
    unittest.main()
