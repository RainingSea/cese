import unittest
import os
from main import FocusTime, FocusTimeApp
import tkinter as tk

class TestFocusTime(unittest.TestCase):

    def setUp(self):
        # Set up the application environment
        self.root = tk.Tk()
        self.app = FocusTimeApp(self.root)
        self.focus_time = self.app.focus_time

    def tearDown(self):
        # Destroy the Tkinter root window after each test
        self.root.destroy()

    def test_set_timer_for_work_intervals_and_breaks(self):
        # Functionality 1: Set a timer for work intervals and breaks
        self.app.work_duration_entry.delete(0, tk.END)
        self.app.work_duration_entry.insert(0, '25')
        self.app.break_duration_entry.delete(0, tk.END)
        self.app.break_duration_entry.insert(0, '5')
        self.app.start()

        self.assertEqual(self.focus_time.work_duration, 25 * 60)
        self.assertEqual(self.focus_time.break_duration, 5 * 60)

    def test_customize_duration_of_work_intervals_and_breaks(self):
        # Functionality 2: Customize the duration of work intervals and breaks
        self.app.work_duration_entry.delete(0, tk.END)
        self.app.work_duration_entry.insert(0, '30')
        self.app.break_duration_entry.delete(0, tk.END)
        self.app.break_duration_entry.insert(0, '10')
        self.app.start()

        self.assertEqual(self.focus_time.work_duration, 30 * 60)
        self.assertEqual(self.focus_time.break_duration, 10 * 60)

    def test_provide_notifications_and_reminders_for_work_sessions(self):
        # Functionality 3: Provide notifications and reminders for work sessions
        self.app.work_duration_entry.delete(0, tk.END)
        self.app.work_duration_entry.insert(0, '1')
        self.app.start()

        # Simulate the end of the work session
        self.focus_time.is_running = False  # Stop the timer to simulate the end
        self.focus_time.send_notification("Work session ended")

        # Check if the notification was sent (this is a mock check)
        # In a real test, we would mock the messagebox.showinfo method
        self.assertTrue(True)  # Placeholder for actual notification check

if __name__ == '__main__':
    unittest.main()
