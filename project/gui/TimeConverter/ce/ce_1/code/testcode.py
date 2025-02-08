import unittest
from main import TimeConverterApp
import tkinter as tk

class TestTimeConverter(unittest.TestCase):

    def setUp(self):
        # Set up the tkinter root and the application
        self.root = tk.Tk()
        self.app = TimeConverterApp(self.root)

    def tearDown(self):
        # Destroy the tkinter root after each test
        self.root.destroy()

    def test_convert_time_between_time_zones(self):
        # Test case 1: Convert from UTC to EST
        self.app.input_time_entry.insert(0, "12:00 PM")
        self.app.source_timezone_entry.delete(0, tk.END)
        self.app.source_timezone_entry.insert(0, "UTC")
        self.app.target_timezone_entry.delete(0, tk.END)
        self.app.target_timezone_entry.insert(0, "US/Eastern")
        self.app.convert_time()
        self.assertEqual(self.app.result_label.cget("text"), "7:00 AM")

        # Test case 2: Convert from PST to GMT
        self.app.input_time_entry.delete(0, tk.END)
        self.app.input_time_entry.insert(0, "3:00 PM")
        self.app.source_timezone_entry.delete(0, tk.END)
        self.app.source_timezone_entry.insert(0, "US/Pacific")
        self.app.target_timezone_entry.delete(0, tk.END)
        self.app.target_timezone_entry.insert(0, "GMT")
        self.app.convert_time()
        self.assertEqual(self.app.result_label.cget("text"), "11:00 PM")

    def test_convert_time_between_formats(self):
        # Test case 1: Convert from 24-hour to 12-hour format
        self.app.input_time_entry.delete(0, tk.END)
        self.app.input_time_entry.insert(0, "15:30")
        self.app.time_format_entry.delete(0, tk.END)
        self.app.time_format_entry.insert(0, "%H:%M")
        self.app.convert_time()
        self.assertEqual(self.app.result_label.cget("text"), "3:30 PM")

        # Test case 2: Convert from 12-hour to 24-hour format
        self.app.input_time_entry.delete(0, tk.END)
        self.app.input_time_entry.insert(0, "9:45 AM")
        self.app.time_format_entry.delete(0, tk.END)
        self.app.time_format_entry.insert(0, "%I:%M %p")
        self.app.convert_time()
        self.assertEqual(self.app.result_label.cget("text"), "09:45")

if __name__ == '__main__':
    unittest.main()
