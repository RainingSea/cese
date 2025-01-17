import unittest
from tkinter import Tk
from main import Main
from task_manager import TaskManager

class TestTimeTracker(unittest.TestCase):

    def setUp(self):
        self.app = Main()
        self.app.root = Tk()  # Mock the Tkinter root window
        self.app.task_manager = TaskManager()  # Use a fresh TaskManager instance

    def tearDown(self):
        self.app.root.destroy()

    def test_create_task(self):
        # Functionality 1: Create Tasks
        self.app.title_entry.insert(0, "Task 1")
        self.app.description_entry.insert(0, "Description for Task 1")
        self.app.create_task()
        self.assertEqual(len(self.app.task_manager.tasks), 1)
        self.assertEqual(self.app.task_manager.tasks[0].title, "Task 1")

        # Test creating a task with an empty name
        self.app.title_entry.delete(0, 'end')
        self.app.description_entry.delete(0, 'end')
        self.app.create_task()
        self.assertEqual(len(self.app.task_manager.tasks), 1)  # No new task should be added

    def test_set_timer(self):
        # Functionality 2: Set Timers for Tasks
        self.app.task_manager.create_task("Task 2", "Description for Task 2")
        self.app.update_task_list()
        self.app.task_listbox.select_set(0)
        self.app.start_timer()
        self.assertTrue(self.app.task_manager.tasks[0].is_running)

        # Test setting a timer with an invalid duration
        # Note: The current implementation does not support setting a duration directly
        # This test will fail as the feature is not implemented
        self.fail("Setting timer duration is not implemented")

    def test_set_alarm(self):
        # Functionality 3: Set Alarms for Reminders
        # This feature is not implemented in the codebase
        self.fail("Set alarm feature is not implemented")

    def test_generate_report(self):
        # Functionality 4: Generate Detailed Reports on Time Allocation
        self.app.task_manager.create_task("Task 3", "Description for Task 3")
        report = self.app.task_manager.generate_report()
        self.assertIn("Task 3", report)

        # Test generating a report without any recorded tasks
        self.app.task_manager.tasks = []  # Clear tasks
        report = self.app.task_manager.generate_report()
        self.assertEqual(report, "Task Report:\n")

    def test_provide_insights(self):
        # Functionality 5: Provide Insights to Improve Time Management
        # This feature is not implemented in the codebase
        self.fail("Provide insights feature is not implemented")

if __name__ == '__main__':
    unittest.main()
