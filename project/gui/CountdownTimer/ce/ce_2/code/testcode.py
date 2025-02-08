import unittest
from countdown_timer import CountdownTimer
import tkinter as tk
from tkinter import messagebox

class TestCountdownTimer(unittest.TestCase):

    def setUp(self):
        # Create a mock GUI for testing
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window during tests
        self.gui = GUI()
        self.gui.root = self.root  # Use the mock root

    def tearDown(self):
        self.root.destroy()

    def test_set_specific_amount_of_time(self):
        # Test valid time duration
        self.gui.duration_entry.insert(0, "10")
        self.gui.start_countdown()
        self.assertEqual(self.gui.timer.duration, 10)
        self.assertEqual(self.gui.timer.remaining_time, 10)

        # Test invalid time duration
        self.gui.duration_entry.delete(0, tk.END)
        self.gui.duration_entry.insert(0, "-5")
        with self.assertRaises(ValueError):
            self.gui.start_countdown()

    def test_countdown_to_zero(self):
        # Test countdown from 1 minute
        self.gui.duration_entry.delete(0, tk.END)
        self.gui.duration_entry.insert(0, "1")
        self.gui.start_countdown()
        self.assertEqual(self.gui.timer.remaining_time, 1)

        # Simulate countdown to zero
        self.gui.timer.remaining_time = 0
        self.gui.update_display()
        self.assertEqual(self.gui.countdown_label.cget("text"), "0")

        # Test countdown from 5 seconds
        self.gui.duration_entry.delete(0, tk.END)
        self.gui.duration_entry.insert(0, "5")
        self.gui.start_countdown()
        self.assertEqual(self.gui.timer.remaining_time, 5)

        # Simulate countdown to zero
        self.gui.timer.remaining_time = 0
        self.gui.update_display()
        self.assertEqual(self.gui.countdown_label.cget("text"), "0")

    def test_pause_countdown(self):
        # Test pause functionality
        self.gui.duration_entry.delete(0, tk.END)
        self.gui.duration_entry.insert(0, "10")
        self.gui.start_countdown()
        self.gui.timer.remaining_time = 5  # Simulate countdown
        self.gui.reset_countdown()
        self.assertEqual(self.gui.countdown_label.cget("text"), "")
        self.assertEqual(self.gui.timer.remaining_time, 10)

if __name__ == '__main__':
    unittest.main()
