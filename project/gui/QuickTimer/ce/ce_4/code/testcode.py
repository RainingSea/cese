import unittest
import tkinter as tk
from tkinter import messagebox
from unittest.mock import patch
import threading
import time

# Assuming the Timer and TimerApp classes are defined in a module named quicktimer
from main import Timer, TimerApp

class TestQuickTimer(unittest.TestCase):

    def setUp(self):
        # Initialize the TimerApp for testing
        self.app = TimerApp()
        self.app.root.update()

    def tearDown(self):
        # Destroy the Tkinter root window after each test
        self.app.root.destroy()

    def test_input_valid_time_duration(self):
        # Functionality 1: Input Desired Time Duration
        self.app.duration_entry.insert(0, "5")
        self.assertEqual(self.app.duration_entry.get(), "5")

    def test_input_invalid_time_duration(self):
        # Functionality 1: Input Desired Time Duration
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            self.app.duration_entry.insert(0, "abc")
            self.app.start_timer()
            mock_showerror.assert_called_once_with("Invalid input", "Please enter a valid number.")

    def test_start_timer_single_click(self):
        # Functionality 2: Start Timer with a Single Click
        self.app.duration_entry.insert(0, "10")
        self.app.start_timer()
        self.assertEqual(self.app.countdown_time, 10)

    def test_start_and_stop_timer(self):
        # Functionality 2: Start Timer with a Single Click
        self.app.duration_entry.insert(0, "15")
        self.app.start_timer()
        time.sleep(2)  # Let the timer run for a bit
        self.app.countdown_time = 0  # Simulate stopping the timer
        self.assertEqual(self.app.countdown_time, 0)

    def test_notification_when_timer_reaches_zero(self):
        # Functionality 3: Notifications When Timer Reaches Zero
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.duration_entry.insert(0, "1")
            self.app.start_timer()
            time.sleep(2)  # Wait for the timer to reach zero
            mock_showinfo.assert_called_once_with("Timer Complete", "The timer has finished!")

if __name__ == '__main__':
    unittest.main()
