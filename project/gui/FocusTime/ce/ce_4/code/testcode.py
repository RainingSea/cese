import unittest
from main import FocusTimeApp
from timer import Timer
import tkinter as tk

class TestFocusTimeApp(unittest.TestCase):

    def setUp(self):
        # Initialize the application
        self.app = FocusTimeApp()
        self.app.root.update_idletasks()

    def tearDown(self):
        # Destroy the application instance after each test
        self.app.root.destroy()

    def test_set_timer_for_work_intervals_and_breaks(self):
        # Functionalities 1: Set a timer for work intervals and breaks
        self.app.work_entry.delete(0, tk.END)
        self.app.work_entry.insert(0, '25')
        self.app.break_entry.delete(0, tk.END)
        self.app.break_entry.insert(0, '5')
        
        self.assertEqual(self.app.work_entry.get(), '25')
        self.assertEqual(self.app.break_entry.get(), '5')

        # Start the work interval timer
        self.app.start_timer()
        self.assertEqual(self.app.timer.duration, 25 * 60)

    def test_customize_duration_of_work_intervals_and_breaks(self):
        # Functionalities 2: Customize the duration of work intervals and breaks
        self.app.work_entry.delete(0, tk.END)
        self.app.work_entry.insert(0, '30')
        self.app.break_entry.delete(0, tk.END)
        self.app.break_entry.insert(0, '10')
        
        self.assertEqual(self.app.work_entry.get(), '30')
        self.assertEqual(self.app.break_entry.get(), '10')

        # Start the break timer after completing the work interval
        self.app.start_timer()
        self.app.show_countdown(0)  # Simulate end of work interval
        self.assertEqual(self.app.timer.duration, 10 * 60)

    def test_provide_notifications_and_reminders_for_work_sessions(self):
        # Functionalities 3: Provide notifications and reminders for work sessions
        self.app.work_entry.delete(0, tk.END)
        self.app.work_entry.insert(0, '1')  # Set work interval to 1 minute for testing
        
        # Mock the show_notification method to test notifications
        self.app.show_notification = lambda message: self.assertEqual(message, "Work interval completed!")
        
        # Start the work interval timer
        self.app.start_timer()
        self.app.show_countdown(0)  # Simulate end of work interval

if __name__ == '__main__':
    unittest.main()
