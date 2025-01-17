import unittest
import tkinter as tk
from main import TimerUI, CountdownTimer

class TestCountdownTimer(unittest.TestCase):

    def setUp(self):
        self.app = TimerUI()
        self.app.root.update_idletasks()

    def tearDown(self):
        self.app.root.destroy()

    def test_set_specific_amount_of_time_valid(self):
        # Simulate entering a valid time duration
        self.app.time_entry.insert(0, "600")  # 10 minutes in seconds
        self.app.start_countdown()
        self.assertEqual(self.app.countdown_timer.remaining_time, 600)

    def test_set_specific_amount_of_time_invalid(self):
        # Simulate entering an invalid time duration
        self.app.time_entry.insert(0, "-300")  # -5 minutes in seconds
        try:
            self.app.start_countdown()
            self.fail("Expected ValueError for negative time duration")
        except ValueError:
            pass  # Expected outcome

    def test_countdown_to_zero(self):
        # Simulate setting a specific amount of time and starting the countdown
        self.app.time_entry.insert(0, "5")  # 5 seconds
        self.app.start_countdown()
        self.app.root.update_idletasks()
        time.sleep(6)  # Wait for countdown to finish
        self.assertEqual(self.app.countdown_timer.remaining_time, 0)

    def test_pause_functionality(self):
        # Simulate starting the countdown and then pausing it
        self.app.time_entry.insert(0, "10")  # 10 seconds
        self.app.start_countdown()
        self.app.root.update_idletasks()
        time.sleep(3)  # Let it run for 3 seconds
        self.app.reset_countdown()  # Simulate stop/pause
        self.assertTrue(0 < self.app.countdown_timer.remaining_time < 10)

if __name__ == '__main__':
    unittest.main()
