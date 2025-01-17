import unittest
from TimeTracker import TimeTracker
from Task import Task

class TestTimeTrackerApp(unittest.TestCase):

    def setUp(self):
        self.tracker = TimeTracker()

    def test_create_task(self):
        # Functionality 1: Create Tasks
        self.tracker.add_task("Task 1", "Description 1")
        self.assertEqual(len(self.tracker.tasks), 1)
        self.assertEqual(self.tracker.tasks[0].title, "Task 1")
        
        # Attempt to create a task with an empty name
        with self.assertRaises(ValueError):
            self.tracker.add_task("", "Description 2")

    def test_set_timer_for_task(self):
        # Functionality 2: Set Timers for Tasks
        self.tracker.add_task("Task 1", "Description 1")
        task_id = 1
        task = self.tracker.get_task_by_id(task_id)
        
        # Start timer for a valid task
        self.tracker.start_timer(task_id)
        self.assertTrue(task.is_active)
        
        # Attempt to set a timer with an invalid duration
        with self.assertRaises(ValueError):
            task.duration = -30  # Simulating invalid duration

    def test_set_alarm(self):
        # Functionality 3: Set Alarms for Reminders
        self.tracker.set_alarm("14:30", "Meeting Reminder")
        self.assertEqual(len(self.tracker.alarms), 1)
        
        # Attempt to set an alarm for a past time
        with self.assertRaises(ValueError):
            self.tracker.set_alarm("00:00", "Past Alarm")

    def test_generate_report(self):
        # Functionality 4: Generate Detailed Reports on Time Allocation
        self.tracker.add_task("Task 1", "Description 1")
        report = self.tracker.generate_report()
        self.assertIn("Task: Task 1", report)
        
        # Attempt to generate a report without any recorded tasks
        empty_tracker = TimeTracker()
        report = empty_tracker.generate_report()
        self.assertEqual(report, "Task Report:\n")

    def test_provide_insights(self):
        # Functionality 5: Provide Insights to Improve Time Management
        self.fail("not implemented")

if __name__ == '__main__':
    unittest.main()
