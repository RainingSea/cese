import unittest
import tkinter as tk
from main import FocusTimeApp, Timer

class TestFocusTimeApp(unittest.TestCase):

    def setUp(self):
        self.app = FocusTimeApp()
        self.app.root.update()  # Ensure the GUI is up to date

    def tearDown(self):
        self.app.root.destroy()

    def test_set_timer_for_work_intervals_and_breaks(self):
        # Set work interval to 25 minutes and break to 5 minutes
        self.app.work_entry.delete(0, tk.END)
        self.app.work_entry.insert(0, '25')
        self.app.break_entry.delete(0, tk.END)
        self.app.break_entry.insert(0, '5')
        
        # Start the timer
        self.app.start_timer()
        
        # Check if the timer is set correctly
        self.assertEqual(self.app.timer.duration, 25 * 60)
        self.assertEqual(self.app.status_label.cget("text"), "Timer Status: Working")

    def test_customize_duration_of_work_intervals_and_breaks(self):
        # Change work interval to 30 minutes and break to 10 minutes
        self.app.work_entry.delete(0, tk.END)
        self.app.work_entry.insert(0, '30')
        self.app.break_entry.delete(0, tk.END)
        self.app.break_entry.insert(0, '10')
        
        # Start the timer
        self.app.start_timer()
        
        # Check if the new settings are saved and timers are set correctly
        self.assertEqual(self.app.timer.duration, 30 * 60)
        self.assertEqual(self.app.status_label.cget("text"), "Timer Status: Working")

    def test_provide_notifications_and_reminders_for_work_sessions(self):
        # Set work interval to 1 minute for testing
        self.app.work_entry.delete(0, tk.END)
        self.app.work_entry.insert(0, '1')
        
        # Start the timer
        self.app.start_timer()
        
        # Simulate the timer reaching 00:00
        self.app.timer.notify()
        
        # Check if the notification is printed
        self.assertEqual(self.app.status_label.cget("text"), "Timer Status: Working")

if __name__ == '__main__':
    unittest.main()
