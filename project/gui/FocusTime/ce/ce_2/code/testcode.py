import unittest
from unittest.mock import patch
from main import MainApp
from PomodoroTimer import PomodoroTimer

class TestFocusTimeApp(unittest.TestCase):

    def setUp(self):
        # Initialize the MainApp instance for testing
        self.app = MainApp()

    def test_set_timer_for_work_intervals_and_breaks(self):
        # Functionalities 1: Set a timer for work intervals and breaks
        self.app.work_entry.delete(0, 'end')
        self.app.work_entry.insert(0, '25')
        self.app.break_entry.delete(0, 'end')
        self.app.break_entry.insert(0, '5')
        
        self.app.start_button_clicked()
        
        self.assertEqual(self.app.timer.work_duration, 25 * 60)
        self.assertEqual(self.app.timer.break_duration, 5 * 60)

    def test_customize_duration_of_work_intervals_and_breaks(self):
        # Functionalities 2: Customize the duration of work intervals and breaks
        self.app.work_entry.delete(0, 'end')
        self.app.work_entry.insert(0, '30')
        self.app.break_entry.delete(0, 'end')
        self.app.break_entry.insert(0, '10')
        
        self.app.start_button_clicked()
        
        self.assertEqual(self.app.timer.work_duration, 30 * 60)
        self.assertEqual(self.app.timer.break_duration, 10 * 60)

    @patch('tkinter.messagebox.showinfo')
    def test_provide_notifications_and_reminders_for_work_sessions(self, mock_showinfo):
        # Functionalities 3: Provide notifications and reminders for work sessions
        self.app.work_entry.delete(0, 'end')
        self.app.work_entry.insert(0, '1')  # Set work interval to 1 minute for testing
        self.app.break_entry.delete(0, 'end')
        self.app.break_entry.insert(0, '1')  # Set break interval to 1 minute for testing
        
        self.app.start_button_clicked()
        
        # Simulate the timer reaching 0
        self.app.timer.remaining_time = 0
        self.app.timer.notify_user()
        
        # Check if the notification was shown
        mock_showinfo.assert_called_with("Pomodoro Timer", "Time's up! Take a break!")

if __name__ == '__main__':
    unittest.main()
