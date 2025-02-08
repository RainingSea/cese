import unittest
from main import CountdownTimer

class TestCountdownTimer(unittest.TestCase):

    def setUp(self):
        # Initialize the CountdownTimer with a default duration
        self.timer = CountdownTimer(60)  # 1 minute for initial setup

    def test_set_specific_amount_of_time(self):
        # Test setting a valid time duration
        self.timer.duration = 600  # 10 minutes
        self.assertEqual(self.timer.duration, 600)

        # Test setting an invalid time duration
        with self.assertRaises(ValueError):
            self.timer.duration = -300  # -5 minutes

    def test_countdown_to_zero(self):
        # Test countdown from a specific time to zero
        self.timer.duration = 5  # 5 seconds
        self.timer.start_timer()
        self.assertEqual(self.timer.remaining_time, 0)

    def test_pause_timer(self):
        # Test pausing the timer
        self.timer.duration = 10  # 10 seconds
        self.timer.start_timer()
        time.sleep(3)  # Let the timer run for 3 seconds
        self.timer.is_running = False  # Simulate stop
        self.assertTrue(self.timer.remaining_time > 0)
        self.assertEqual(self.timer.is_running, False)

if __name__ == '__main__':
    unittest.main()
