import unittest
from task_manager import TaskManager
from notification_manager import NotificationManager
import os

class TestBusinessTaskScheduler(unittest.TestCase):

    def setUp(self):
        # Setup for TaskManager and NotificationManager
        self.task_manager = TaskManager()
        self.notification_manager = NotificationManager()

    def test_create_tasks(self):
        # Functionalities 1: Create Tasks
        initial_task_count = len(self.task_manager.get_tasks())
        self.task_manager.create_task("Prepare Report", "Compile monthly sales data", "Medium", "John Doe", "2023-12-31")
        self.assertEqual(len(self.task_manager.get_tasks()), initial_task_count + 1)
        self.assertEqual(self.task_manager.get_tasks()[-1].title, "Prepare Report")

    def test_assign_tasks_to_team_members(self):
        # Functionalities 2: Assign Tasks to Team Members
        self.task_manager.create_task("Task for Assignment", "Description", "Medium", "John Doe", "2023-12-31")
        task = self.task_manager.get_tasks()[-1]
        self.assertEqual(task.assignee, "John Doe")

    def test_set_deadlines_for_tasks(self):
        # Functionalities 3: Set Deadlines for Tasks
        self.task_manager.create_task("Deadline Task", "Description", "Medium", "John Doe", "2023-12-31")
        task = self.task_manager.get_tasks()[-1]
        self.assertEqual(task.deadline, "2023-12-31")

    def test_track_task_progress(self):
        # Functionalities 4: Track Task Progress
        self.task_manager.create_task("Progress Task", "Description", "Medium", "John Doe", "2023-12-31")
        task_title = "Progress Task"
        self.task_manager.update_task_status(task_title, "In Progress")
        task = next((t for t in self.task_manager.get_tasks() if t.title == task_title), None)
        self.assertEqual(task.status, "In Progress")
        self.task_manager.update_task_status(task_title, "Completed")
        self.assertEqual(task.status, "Completed")

    def test_prioritize_tasks(self):
        # Functionalities 5: Prioritize Tasks
        self.task_manager.create_task("Priority Task", "Description", "Low", "John Doe", "2023-12-31")
        task = self.task_manager.get_tasks()[-1]
        self.assertEqual(task.priority, "Low")
        task.priority = "High"
        self.task_manager.save_tasks()
        self.assertEqual(task.priority, "High")

    def test_send_notifications_for_tasks(self):
        # Functionalities 6: Send Notifications for Tasks
        self.notification_manager.add_notification("Test Notification")
        self.assertIn("Test Notification", self.notification_manager.get_notifications())

    def test_integrate_with_calendar_for_task_scheduling(self):
        # Functionalities 7: Integrate with a Calendar for Task Scheduling
        self.fail("not implemented")

if __name__ == '__main__':
    unittest.main()
