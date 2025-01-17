import unittest
from pywinauto import Application
from pywinauto.timings import wait_until_passes
import time

class TestQuickTimer(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.app = Application(backend="tk").start("python D:/Project/CE/CE/project/gui/QuickTimer/ce/ce_2/code/main.py")
        self.main_window = self.app.QuickTimer

    def tearDown(self):
        # Close the application
        self.app.kill()

    def test_input_desired_time_duration(self):
        # Test valid input
        self.main_window.child_window(auto_id="!entry").type_keys("5")
        self.assertEqual(self.main_window.child_window(auto_id="!entry").get_value(), "5")

        # Test invalid input
        self.main_window.child_window(auto_id="!entry").type_keys("abc")
        self.main_window.child_window(auto_id="!button").click()
        self.assertTrue(self.main_window.child_window(title="Invalid input").exists())

    def test_start_timer_with_single_click(self):
        # Test timer starts and button changes to "Stop Timer"
        self.main_window.child_window(auto_id="!entry").type_keys("10")
        self.main_window.child_window(auto_id="!button").click()
        time.sleep(1)  # Wait a bit to ensure the timer starts
        self.assertTrue(self.main_window.child_window(title="Stop Timer").exists())

        # Test timer stops and countdown is paused
        self.main_window.child_window(auto_id="!button").click()
        time_left = self.main_window.child_window(auto_id="!label").window_text()
        time.sleep(2)
        self.assertEqual(self.main_window.child_window(auto_id="!label").window_text(), time_left)

    def test_notifications_when_timer_reaches_zero(self):
        # Test short duration notification
        self.main_window.child_window(auto_id="!entry").type_keys("5")
        self.main_window.child_window(auto_id="!button").click()
        wait_until_passes(10, 1, lambda: self.main_window.child_window(title="Time's up!").exists())
        self.assertTrue(self.main_window.child_window(title="Time's up!").exists())

        # Test longer duration notification
        self.main_window.child_window(auto_id="!entry").type_keys("60")
        self.main_window.child_window(auto_id="!button").click()
        wait_until_passes(70, 1, lambda: self.main_window.child_window(title="Time's up!").exists())
        self.assertTrue(self.main_window.child_window(title="Time's up!").exists())

if __name__ == '__main__':
    unittest.main()
