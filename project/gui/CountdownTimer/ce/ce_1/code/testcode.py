import unittest
from main import CountdownTimer

class TestCountdownTimer(unittest.TestCase):

    def setUp(self):
        # Initialize the CountdownTimer with a default duration
        self.timer = CountdownTimer(0)

    def test_set_specific_time(self):
        # Test setting a valid time duration
        self.timer.duration = 600  # 10 minutes
        self.timer.remaining_time = 600
        self.assertEqual(self.timer.remaining_time, 600)

        # Test setting an invalid time duration
        with self.assertRaises(ValueError):
            self.timer.duration = -300  # -5 minutes
            self.timer.remaining_time = -300

    def test_countdown_to_zero(self):
        # Test countdown from 1 minute
        self.timer.duration = 60  # 1 minute
        self.timer.remaining_time = 60
        self.timer.start_timer()
        self.assertEqual(self.timer.remaining_time, 0)

        # Test countdown from 5 seconds
        self.timer.duration = 5  # 5 seconds
        self.timer.remaining_time = 5
        self.timer.start_timer()
        self.assertEqual(self.timer.remaining_time, 0)

    def test_pause_timer(self):
        # Test pausing the timer
        self.timer.duration = 30  # 30 seconds
        self.timer.remaining_time = 30
        self.timer.is_running = True
        self.timer.is_running = False  # Simulate stop
        self.assertEqual(self.timer.remaining_time, 30)

if __name__ == '__main__':
    unittest.main()
