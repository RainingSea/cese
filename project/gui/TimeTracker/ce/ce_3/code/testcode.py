import unittest
from task_manager import TaskManager
from timer_manager import TimerManager
from report_generator import ReportGenerator

class TestTimeTracker(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()
        self.timer_manager = TimerManager()
        self.report_generator = ReportGenerator()

    def test_create_task(self):
        # Functionality 1: Create Tasks
        # Test creating a task with a valid name and description
        self.task_manager.create_task("Task 1", "Description 1")
        self.assertEqual(len(self.task_manager.tasks), 1)
        self.assertEqual(self.task_manager.tasks[0].title, "Task 1")

        # Test creating a task with an empty name
        with self.assertRaises(ValueError):
            self.task_manager.create_task("", "Description 2")

    def test_set_timer(self):
        # Functionality 2: Set Timers for Tasks
        self.timer_manager.start_timer("Task 1")
        self.assertEqual(len(self.timer_manager.timers), 1)
        self.assertEqual(self.timer_manager.timers[0].task_title, "Task 1")

        # Test setting a timer with an invalid duration (negative duration)
        with self.assertRaises(ValueError):
            self.timer_manager.start_timer("Task 2", -30)

    def test_set_alarm(self):
        # Functionality 3: Set Alarms for Reminders
        # This functionality is not implemented in the codebase
        self.fail("Set Alarms for Reminders functionality not implemented")

    def test_generate_report(self):
        # Functionality 4: Generate Detailed Reports on Time Allocation
        report = self.report_generator.generate_report()
        self.assertIn("Task Report:", report)

        # Test generating a report without any recorded tasks
        self.task_manager.tasks = []  # Clear tasks
        report = self.report_generator.generate_report()
        self.assertIn("No timers recorded.", report)

    def test_provide_insights(self):
        # Functionality 5: Provide Insights to Improve Time Management
        # This functionality is not implemented in the codebase
        self.fail("Provide Insights to Improve Time Management functionality not implemented")

if __name__ == '__main__':
    unittest.main()
