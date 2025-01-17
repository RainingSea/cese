import unittest
from CountdownTimer import CountdownTimer
import tkinter as tk
from main import UI

class TestCountdownTimer(unittest.TestCase):

    def setUp(self):
        self.ui = UI()
        self.ui.root.update()  # Ensure the Tkinter main loop is updated

    def tearDown(self):
        self.ui.root.destroy()

    def test_set_specific_amount_of_time_for_countdown(self):
        # Test valid time input
        self.ui.entry.insert(0, "600")  # 10 minutes
        self.ui.start_countdown()
        self.assertEqual(self.ui.timer.duration, 600)
        self.assertEqual(self.ui.timer.remaining_time, 600)

        # Test invalid time input
        self.ui.entry.delete(0, tk.END)
        self.ui.entry.insert(0, "-300")  # -5 minutes
        with self.assertRaises(ValueError):
            self.ui.start_countdown()

    def test_countdown_to_zero_once_started(self):
        # Test countdown decrementing
        self.ui.entry.insert(0, "60")  # 1 minute
        self.ui.start_countdown()
        self.assertEqual(self.ui.timer.remaining_time, 60)
        self.ui.timer.remaining_time = 0  # Simulate countdown reaching zero
        self.ui.update_display()
        self.assertEqual(self.ui.time_display.cget("text"), "Time remaining: 0 seconds")

        # Test countdown completion message
        self.ui.entry.delete(0, tk.END)
        self.ui.entry.insert(0, "5")  # 5 seconds
        self.ui.start_countdown()
        self.ui.timer.remaining_time = 0  # Simulate countdown reaching zero
        self.ui.update_display()
        self.assertEqual(self.ui.time_display.cget("text"), "Time remaining: 0 seconds")

    def test_pause_countdown(self):
        # Test pause functionality
        self.ui.entry.insert(0, "30")  # 30 seconds
        self.ui.start_countdown()
        self.ui.timer.remaining_time = 15  # Simulate countdown running
        self.ui.reset_countdown()
        self.assertEqual(self.ui.timer.remaining_time, 30)  # Timer reset to initial value

if __name__ == '__main__':
    unittest.main()
