import unittest
import tkinter as tk
from main import QuickTimer

class TestQuickTimer(unittest.TestCase):

    def setUp(self):
        self.app = QuickTimer()
        self.app.window.update()  # Ensure the GUI is updated

    def tearDown(self):
        self.app.window.destroy()

    def test_input_desired_time_duration(self):
        # Test valid input
        self.app.duration_entry.delete(0, tk.END)
        self.app.duration_entry.insert(0, "5")
        self.app.start_timer()
        self.assertEqual(self.app.duration, 5)

        # Test invalid input
        self.app.duration_entry.delete(0, tk.END)
        self.app.duration_entry.insert(0, "abc")
        self.app.start_timer()
        self.assertEqual(self.app.timer_label.cget("text"), "Please enter a valid number.")

    def test_start_timer_with_single_click(self):
        # Test start timer
        self.app.duration_entry.delete(0, tk.END)
        self.app.duration_entry.insert(0, "10")
        self.app.start_timer()
        self.assertEqual(self.app.duration, 10)

        # Test stop timer (not implemented in the codebase)
        self.fail("Stop timer functionality not implemented")

    def test_notifications_when_timer_reaches_zero(self):
        # Test notification for short duration
        self.app.duration_entry.delete(0, tk.END)
        self.app.duration_entry.insert(0, "1")
        self.app.start_timer()
        self.app.window.after(1100, self.assertEqual, self.app.timer_label.cget("text"), "0")

        # Test notification for longer duration (not implemented in the codebase)
        self.fail("Notification for longer duration not implemented")

if __name__ == '__main__':
    unittest.main()
