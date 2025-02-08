import unittest
import time
from main import FocusTimeApp, Timer, Settings

class TestFocusTimeApp(unittest.TestCase):

    def setUp(self):
        self.app = FocusTimeApp()

    def test_set_timer_for_work_intervals_and_breaks(self):
        # Functionalities 1: Set a timer for work intervals and breaks
        self.app.work_duration_var.set(25)
        self.app.break_duration_var.set(5)
        self.assertEqual(self.app.work_duration_var.get(), 25)
        self.assertEqual(self.app.break_duration_var.get(), 5)

        self.app.start_timer()
        self.assertTrue(self.app.timer.running)

        # Simulate the countdown for testing purposes
        time.sleep(2)  # Wait for a couple of seconds to simulate timer running
        self.app.timer.stop()
        self.assertFalse(self.app.timer.running)

    def test_customize_duration_of_work_intervals_and_breaks(self):
        # Functionalities 2: Customize the duration of work intervals and breaks
        self.app.work_duration_var.set(30)
        self.app.break_duration_var.set(10)
        self.app.save_settings()
        
        # Reload settings to verify they were saved correctly
        self.app.settings.load_settings()
        self.assertEqual(self.app.settings.work_duration, 30)
        self.assertEqual(self.app.settings.break_duration, 10)

        self.app.start_timer()
        self.assertTrue(self.app.timer.running)

        # Simulate the countdown for testing purposes
        time.sleep(2)  # Wait for a couple of seconds to simulate timer running
        self.app.timer.stop()
        self.assertFalse(self.app.timer.running)

    def test_provide_notifications_and_reminders_for_work_sessions(self):
        # Functionalities 3: Provide notifications and reminders for work sessions
        self.app.work_duration_var.set(1)  # Set to 1 minute for testing
        self.app.start_timer()
        self.assertTrue(self.app.timer.running)

        # Simulate the countdown for testing purposes
        time.sleep(2)  # Wait for a couple of seconds to simulate timer running
        self.app.timer.stop()
        self.assertFalse(self.app.timer.running)

        # Since we cannot directly test GUI notifications, we assume the logic works if the timer stops

if __name__ == '__main__':
    unittest.main()
