import unittest
from tkinter import Tk
from main import GUI

class TestCountdownTimer(unittest.TestCase):

    def setUp(self):
        # Initialize the GUI application
        self.app = GUI()
        self.app.root.update()

    def tearDown(self):
        # Destroy the Tkinter root window after each test
        self.app.root.destroy()

    def test_set_specific_amount_of_time_for_countdown(self):
        # Test valid time input
        self.app.entry.insert(0, "600")  # 10 minutes in seconds
        self.app.start_countdown()
        self.assertEqual(self.app.timer.countdown_time, 600)
        self.assertEqual(self.app.timer.remaining_time, 600)

        # Test invalid time input
        self.app.entry.delete(0, 'end')
        self.app.entry.insert(0, "-300")  # -5 minutes in seconds
        with self.assertRaises(ValueError):
            self.app.start_countdown()

    def test_countdown_to_zero_once_started(self):
        # Test countdown from 1 minute
        self.app.entry.insert(0, "60")  # 1 minute in seconds
        self.app.start_countdown()
        self.assertTrue(self.app.timer.running)
        self.app.timer.remaining_time = 0  # Simulate countdown reaching zero
        self.app.update_display()
        self.assertEqual(self.app.label.cget("text"), "Remaining Time: 0 seconds")

        # Test countdown from 5 seconds
        self.app.entry.delete(0, 'end')
        self.app.entry.insert(0, "5")  # 5 seconds
        self.app.start_countdown()
        self.app.timer.remaining_time = 0  # Simulate countdown reaching zero
        self.app.update_display()
        self.assertEqual(self.app.label.cget("text"), "Remaining Time: 0 seconds")

    def test_pause_countdown(self):
        # Test pause functionality
        self.app.entry.insert(0, "60")  # 1 minute in seconds
        self.app.start_countdown()
        self.app.timer.running = False  # Simulate pause
        self.assertFalse(self.app.timer.running)
        self.assertEqual(self.app.timer.update_timer(), self.app.timer.remaining_time)

if __name__ == '__main__':
    unittest.main()
