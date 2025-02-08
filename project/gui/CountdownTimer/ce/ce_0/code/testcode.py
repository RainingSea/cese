import unittest
from main import CountdownTimer, GUI
import tkinter as tk

class TestCountdownTimer(unittest.TestCase):

    def setUp(self):
        self.gui = GUI()
        self.gui.root.update()

    def tearDown(self):
        self.gui.root.destroy()

    def test_set_specific_amount_of_time_for_countdown(self):
        # Test valid time duration
        self.gui.entry.delete(0, tk.END)
        self.gui.entry.insert(0, "600")  # 10 minutes in seconds
        self.gui.start_button_clicked()
        self.assertEqual(self.gui.timer.duration, 600)
        self.assertEqual(self.gui.timer.remaining_time, 600)
        self.assertEqual(self.gui.timer_label.cget("text"), "Last duration: 600 seconds")

        # Test invalid time duration
        self.gui.entry.delete(0, tk.END)
        self.gui.entry.insert(0, "-300")  # -5 minutes in seconds
        self.gui.start_button_clicked()
        self.assertEqual(self.gui.timer_label.cget("text"), "Please enter a valid number.")

    def test_countdown_to_zero_once_timer_started(self):
        # Test countdown from 1 minute
        self.gui.entry.delete(0, tk.END)
        self.gui.entry.insert(0, "60")  # 1 minute in seconds
        self.gui.start_button_clicked()
        self.gui.update_timer()
        self.assertEqual(self.gui.timer.remaining_time, 59)

        # Test countdown from 5 seconds
        self.gui.entry.delete(0, tk.END)
        self.gui.entry.insert(0, "5")  # 5 seconds
        self.gui.start_button_clicked()
        self.gui.update_timer()
        self.gui.root.after(5000, self.gui.update_timer)  # Simulate waiting for 5 seconds
        self.assertEqual(self.gui.timer_label.cget("text"), "Time's up!")

        # Test stop functionality (not implemented in the codebase)
        self.fail("Stop functionality not implemented")

if __name__ == '__main__':
    unittest.main()
