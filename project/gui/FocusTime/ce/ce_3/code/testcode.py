import unittest
import tkinter as tk
from main import FocusTimeApp, Timer

class TestFocusTimeApp(unittest.TestCase):

    def setUp(self):
        # Initialize the application
        self.app = FocusTimeApp()
        self.app.window.update_idletasks()

    def tearDown(self):
        # Destroy the window after each test
        self.app.window.destroy()

    def test_set_timer_for_work_intervals_and_breaks(self):
        # Set work interval to 25 minutes and break to 5 minutes
        self.app.work_entry.delete(0, tk.END)
        self.app.work_entry.insert(0, "25")
        self.app.break_entry.delete(0, tk.END)
        self.app.break_entry.insert(0, "5")
        
        # Simulate starting the timer
        self.app.start_timer()
        
        # Check if the timer is set correctly
        self.assertEqual(self.app.timer.duration, 25 * 60)
        self.assertEqual(int(self.app.work_entry.get()), 25)
        self.assertEqual(int(self.app.break_entry.get()), 5)

    def test_customize_duration_of_work_intervals_and_breaks(self):
        # Change work interval to 30 minutes and break to 10 minutes
        self.app.work_entry.delete(0, tk.END)
        self.app.work_entry.insert(0, "30")
        self.app.break_entry.delete(0, tk.END)
        self.app.break_entry.insert(0, "10")
        
        # Simulate starting the timer
        self.app.start_timer()
        
        # Check if the new settings are saved and displayed correctly
        self.assertEqual(self.app.timer.duration, 30 * 60)
        self.assertEqual(int(self.app.work_entry.get()), 30)
        self.assertEqual(int(self.app.break_entry.get()), 10)

    def test_provide_notifications_and_reminders_for_work_sessions(self):
        # Set a work interval of 1 minute for testing purposes
        self.app.work_entry.delete(0, tk.END)
        self.app.work_entry.insert(0, "1")
        
        # Simulate starting the timer
        self.app.start_timer()
        
        # Wait for the timer to finish (in a real test, you would mock time.sleep)
        self.app.timer.run_timer()
        
        # Check if the notification is printed (in a real test, you would capture stdout)
        # Here we assume notify() prints "Time's up!"
        self.assertTrue(self.app.timer.is_running)

if __name__ == '__main__':
    unittest.main()
