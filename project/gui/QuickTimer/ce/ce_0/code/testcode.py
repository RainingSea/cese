import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from main import TimerApp

class TestQuickTimer(unittest.TestCase):

    def setUp(self):
        # Initialize the TimerApp without starting the main loop
        self.app = TimerApp()
        self.app.root = MagicMock()  # Mock the Tkinter root to prevent actual GUI operations

    def test_input_desired_time_duration(self):
        # Test valid input
        self.app.entry.insert(0, "5")
        self.app.start_timer()
        self.assertEqual(self.app.duration, 5)
        self.assertEqual(self.app.remaining_time, 5)

        # Test invalid input
        self.app.entry.delete(0, tk.END)
        self.app.entry.insert(0, "abc")
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            self.app.start_timer()
            mock_showerror.assert_called_once_with("Input Error", "Please enter a valid number.")

    def test_start_timer_with_single_click(self):
        # Test starting the timer
        self.app.entry.insert(0, "10")
        self.app.start_timer()
        self.assertTrue(self.app.is_running)
        self.assertEqual(self.app.remaining_time, 10)

        # Test stopping the timer
        self.app.is_running = False
        self.assertFalse(self.app.is_running)

    def test_notifications_when_timer_reaches_zero(self):
        # Mock the notification to prevent actual notifications
        with patch('plyer.notification.notify') as mock_notify:
            # Test notification after 5 seconds
            self.app.entry.insert(0, "5")
            self.app.start_timer()
            self.app.remaining_time = 0  # Simulate timer reaching zero
            self.app.update_timer()
            mock_notify.assert_called_with(
                title="Timer Finished",
                message="Your timer has ended!",
                app_name="QuickTimer"
            )

            # Test notification after 1 minute
            self.app.entry.delete(0, tk.END)
            self.app.entry.insert(0, "60")
            self.app.start_timer()
            self.app.remaining_time = 0  # Simulate timer reaching zero
            self.app.update_timer()
            mock_notify.assert_called_with(
                title="Timer Finished",
                message="Your timer has ended!",
                app_name="QuickTimer"
            )

if __name__ == '__main__':
    unittest.main()
