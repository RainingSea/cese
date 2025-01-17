import unittest
import tkinter as tk
from countdown_timer import CountdownTimer
from main import UI

class TestCountdownTimer(unittest.TestCase):

    def setUp(self):
        # Set up the UI for testing
        self.app = UI()
        self.app.window.update_idletasks()

    def tearDown(self):
        # Destroy the UI after each test
        self.app.window.destroy()

    def test_set_specific_amount_of_time(self):
        # Test valid time duration
        self.app.duration_entry.insert(0, "600")  # 10 minutes in seconds
        self.app.start_countdown()
        self.assertEqual(self.app.timer.duration, 600)
        self.assertEqual(self.app.timer.remaining_time, 600)

        # Test invalid time duration
        self.app.duration_entry.delete(0, tk.END)
        self.app.duration_entry.insert(0, "-300")  # -5 minutes in seconds
        with self.assertRaises(ValueError):
            self.app.start_countdown()

    def test_countdown_to_zero(self):
        # Test countdown from 1 minute
        self.app.duration_entry.insert(0, "60")  # 1 minute in seconds
        self.app.start_countdown()
        self.assertTrue(self.app.timer.is_running)
        self.app.timer.remaining_time = 0  # Simulate countdown reaching zero
        self.app.update_time()
        self.assertEqual(self.app.time_label.cget("text"), "Remaining Time: 0")

        # Test countdown from 5 seconds
        self.app.duration_entry.delete(0, tk.END)
        self.app.duration_entry.insert(0, "5")  # 5 seconds
        self.app.start_countdown()
        self.app.timer.remaining_time = 0  # Simulate countdown reaching zero
        self.app.update_time()
        self.assertEqual(self.app.time_label.cget("text"), "Remaining Time: 0")

    def test_pause_countdown(self):
        # Test pause functionality
        self.app.duration_entry.insert(0, "60")  # 1 minute in seconds
        self.app.start_countdown()
        self.app.timer.is_running = False  # Simulate pause
        self.app.update_time()
        self.assertFalse(self.app.timer.is_running)
        self.assertEqual(self.app.time_label.cget("text"), "Remaining Time: 60")

if __name__ == '__main__':
    unittest.main()
