import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from main import Main
from task_manager import TaskManager

class TestTimeTracker(unittest.TestCase):

    def setUp(self):
        self.app = Main()
        self.app.root.update()

    def tearDown(self):
        self.app.root.destroy()

    def test_create_task(self):
        # Functionality 1: Create Tasks
        # Test creating a valid task
        self.app.title_entry.insert(0, "Task 1")
        self.app.description_entry.insert(0, "Description 1")
        self.app.add_task()
        self.assertEqual(len(self.app.task_manager.tasks), 1)
        self.assertEqual(self.app.task_manager.tasks[0].title, "Task 1")
        self.assertEqual(self.app.task_manager.tasks[0].description, "Description 1")

        # Test creating a task with an empty name
        self.app.title_entry.delete(0, tk.END)
        self.app.description_entry.delete(0, tk.END)
        with patch('tkinter.messagebox.showwarning') as mock_warning:
            self.app.add_task()
            mock_warning.assert_called_with("Input Error", "Please enter both title and description.")

    def test_set_timer(self):
        # Functionality 2: Set Timers for Tasks
        self.fail("Functionality not implemented: Set Timers for Tasks")

    def test_set_alarm(self):
        # Functionality 3: Set Alarms for Reminders
        self.fail("Functionality not implemented: Set Alarms for Reminders")

    def test_generate_report(self):
        # Functionality 4: Generate Detailed Reports on Time Allocation
        # Test generating a report with tasks
        self.app.task_manager.add_task("Task 1", "Description 1")
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.app.show_report()
            mock_info.assert_called_once()

        # Test generating a report without tasks
        self.app.task_manager.tasks.clear()
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.app.show_report()
            mock_info.assert_called_once_with("Report", "")

    def test_get_insights(self):
        # Functionality 5: Provide Insights to Improve Time Management
        self.fail("Functionality not implemented: Provide Insights to Improve Time Management")

if __name__ == '__main__':
    unittest.main()
