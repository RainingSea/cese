import unittest
from main import CountdownTimer, UI

class TestCountdownTimer(unittest.TestCase):

    def setUp(self):
        self.ui = UI()

    def test_set_specific_amount_of_time(self):
        # Test valid time duration
        self.ui.entry.insert(0, "600")  # 10 minutes in seconds
        self.ui.start_button_clicked()
        self.assertEqual(self.ui.timer.remaining_time, 600)
        self.assertEqual(self.ui.label.cget("text"), "Remaining Time: 600")

        # Test invalid time duration
        self.ui.entry.delete(0, 'end')
        self.ui.entry.insert(0, "-300")  # -5 minutes in seconds
        with self.assertRaises(ValueError):
            self.ui.start_button_clicked()

    def test_countdown_to_zero(self):
        # Test countdown decrement
        self.ui.entry.delete(0, 'end')
        self.ui.entry.insert(0, "60")  # 1 minute in seconds
        self.ui.start_button_clicked()
        self.assertEqual(self.ui.timer.remaining_time, 60)

        # Simulate countdown to zero
        self.ui.timer.remaining_time = 0
        self.ui.update_display(self.ui.timer.remaining_time)
        self.assertEqual(self.ui.label.cget("text"), "Remaining Time: 0")

        # Test countdown finishes
        self.ui.entry.delete(0, 'end')
        self.ui.entry.insert(0, "5")  # 5 seconds
        self.ui.start_button_clicked()
        self.ui.timer.remaining_time = 0
        self.ui.update_display(self.ui.timer.remaining_time)
        self.assertEqual(self.ui.label.cget("text"), "Remaining Time: 0")

    def test_pause_countdown(self):
        # Test pause functionality (not implemented in the codebase)
        self.fail("Pause functionality not implemented")

if __name__ == '__main__':
    unittest.main()
