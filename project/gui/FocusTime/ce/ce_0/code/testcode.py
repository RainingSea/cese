import unittest
import tkinter as tk
from main import FocusTimeApp
from timer import Timer
from unittest.mock import patch

class TestFocusTimeApp(unittest.TestCase):

    def setUp(self):
        # Initialize the application
        self.app = FocusTimeApp()
        self.app.root.update()

    def tearDown(self):
        # Destroy the application after each test
        self.app.root.destroy()

    def test_set_timer_for_work_intervals_and_breaks(self):
        # Functionality 1: Set a timer for work intervals and breaks
        self.app.work_entry.insert(0, "25")
        self.app.break_entry.insert(0, "5")
        self.app.start_timer()

        # Check if the timer is set correctly
        self.assertEqual(self.app.timer.duration, 25 * 60)
        self.assertEqual(self.app.remaining_time_label.cget("text"), "Working for 25 minutes.")

    def test_customize_duration_of_work_intervals_and_breaks(self):
        # Functionality 2: Customize the duration of work intervals and breaks
        self.app.work_entry.insert(0, "30")
        self.app.break_entry.insert(0, "10")
        self.app.start_timer()

        # Check if the new settings are saved and displayed correctly
        self.assertEqual(self.app.timer.duration, 30 * 60)
        self.assertEqual(self.app.remaining_time_label.cget("text"), "Working for 30 minutes.")

    @patch('timer.messagebox.showinfo')
    def test_provide_notifications_and_reminders_for_work_sessions(self, mock_showinfo):
        # Functionality 3: Provide notifications and reminders for work sessions
        self.app.work_entry.insert(0, "1")
        self.app.start_timer()

        # Simulate the timer reaching 0
        self.app.timer.notify()

        # Check if the notification is shown
        mock_showinfo.assert_called_with("FocusTime", "Time's up! Take a break or continue working.")

if __name__ == '__main__':
    unittest.main()
