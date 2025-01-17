import unittest
import tkinter as tk
from main import FocusTimeApp, Timer, Notification

class TestFocusTimeApp(unittest.TestCase):

    def setUp(self):
        # Initialize the application
        self.app = FocusTimeApp()
        self.app.root.update()

    def tearDown(self):
        # Destroy the application instance after each test
        self.app.root.destroy()

    def test_set_timer_for_work_intervals_and_breaks(self):
        # Functionalities 1: Set a timer for work intervals and breaks
        self.app.work_entry.delete(0, tk.END)
        self.app.work_entry.insert(0, "25")
        self.app.break_entry.delete(0, tk.END)
        self.app.break_entry.insert(0, "5")
        
        self.app.start_timer()
        self.app.root.update()

        # Check if the timer is set correctly
        self.assertEqual(self.app.timer.remaining_time, 25 * 60)
        self.assertEqual(self.app.work_duration, 25 * 60)

        # Simulate the timer countdown
        self.app.timer.remaining_time = 0
        self.app.update_timer()
        self.app.root.update()

        # Check if the notification is sent
        self.assertFalse(self.app.timer_running)

    def test_customize_duration_of_work_intervals_and_breaks(self):
        # Functionalities 2: Customize the duration of work intervals and breaks
        self.app.work_entry.delete(0, tk.END)
        self.app.work_entry.insert(0, "30")
        self.app.break_entry.delete(0, tk.END)
        self.app.break_entry.insert(0, "10")
        
        self.app.start_timer()
        self.app.root.update()

        # Check if the new settings are saved
        self.assertEqual(self.app.timer.remaining_time, 30 * 60)
        self.assertEqual(self.app.work_duration, 30 * 60)

        # Simulate the work interval completion
        self.app.timer.remaining_time = 0
        self.app.update_timer()
        self.app.root.update()

        # Start break timer
        self.app.timer = Timer(10 * 60)
        self.app.timer.start()
        self.app.root.update()

        # Simulate the break timer countdown
        self.app.timer.remaining_time = 0
        self.app.update_timer()
        self.app.root.update()

        # Check if the break session is completed
        self.assertFalse(self.app.timer_running)

    def test_provide_notifications_and_reminders_for_work_sessions(self):
        # Functionalities 3: Provide notifications and reminders for work sessions
        self.app.work_entry.delete(0, tk.END)
        self.app.work_entry.insert(0, "1")
        
        self.app.start_timer()
        self.app.root.update()

        # Simulate the timer countdown
        self.app.timer.remaining_time = 0
        self.app.update_timer()
        self.app.root.update()

        # Check if the notification is sent
        self.assertFalse(self.app.timer_running)

if __name__ == '__main__':
    unittest.main()
