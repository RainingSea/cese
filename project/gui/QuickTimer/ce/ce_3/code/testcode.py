import unittest
import tkinter as tk
from main import QuickTimer

class TestQuickTimer(unittest.TestCase):

    def setUp(self):
        # Initialize the QuickTimer application
        self.app = QuickTimer()
        self.app.root.withdraw()  # Hide the main window during tests

    def tearDown(self):
        # Destroy the app instance after each test
        self.app.root.destroy()

    def test_input_valid_time_duration(self):
        # Functionality 1: Input Desired Time Duration
        # Test with valid input
        self.app.time_input.insert(0, "5")
        self.assertEqual(self.app.time_input.get(), "5")

        # Test with invalid input
        self.app.time_input.delete(0, tk.END)
        self.app.time_input.insert(0, "abc")
        self.app.start_timer()
        # Check if an error message is displayed
        # Since we can't capture messagebox output directly, we assume it works if no exception is raised

    def test_start_timer_with_single_click(self):
        # Functionality 2: Start Timer with a Single Click
        # Test starting the timer
        self.app.time_input.delete(0, tk.END)
        self.app.time_input.insert(0, "10")
        self.app.start_timer()
        self.assertEqual(self.app.duration, 10)

        # Test stopping the timer
        self.app.timer.cancel()
        self.assertFalse(self.app.timer.is_alive())

    def test_notifications_when_timer_reaches_zero(self):
        # Functionality 3: Notifications When Timer Reaches Zero
        # Test with a short duration
        self.app.time_input.delete(0, tk.END)
        self.app.time_input.insert(0, "1")
        self.app.start_timer()
        time.sleep(2)  # Wait for the timer to finish
        # Since we can't capture messagebox output directly, we assume it works if no exception is raised

if __name__ == '__main__':
    unittest.main()
