import unittest
from TaskManager import TaskManager
from Task import Task
from User import User

class TestBusinessTaskScheduler(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()

    def test_create_task(self):
        # Functionalities 1: Create Tasks
        task = Task("Prepare Report", "Compile monthly sales data", 3, "2023-12-31")
        self.task_manager.add_task(task)
        self.assertIn(task, self.task_manager.tasks)

    def test_assign_task(self):
        # Functionalities 2: Assign Tasks to Team Members
        task_title = "Task 1"
        user_email = "alice@example.com"
        self.task_manager.assign_task(task_title, user_email)
        task = next((t for t in self.task_manager.tasks if t.title == task_title), None)
        self.assertIsNotNone(task)
        self.assertEqual(task.status, f"Assigned to {user_email}")

    def test_set_deadline(self):
        # Functionalities 3: Set Deadlines for Tasks
        task_title = "Task 1"
        new_deadline = "2024-01-01"
        task = next((t for t in self.task_manager.tasks if t.title == task_title), None)
        if task:
            task.deadline = new_deadline
            self.assertEqual(task.deadline, new_deadline)
        else:
            self.fail("Task not found")

    def test_track_task_progress(self):
        # Functionalities 4: Track Task Progress
        task_title = "Task 1"
        task = next((t for t in self.task_manager.tasks if t.title == task_title), None)
        if task:
            # Update progress to 50%
            task.status = "In Progress 50%"
            self.assertEqual(task.status, "In Progress 50%")

            # Mark as complete
            task.status = "Completed"
            self.assertEqual(task.status, "Completed")
        else:
            self.fail("Task not found")

    def test_prioritize_tasks(self):
        # Functionalities 5: Prioritize Tasks
        task_title = "Task 1"
        task = next((t for t in self.task_manager.tasks if t.title == task_title), None)
        if task:
            # Assign high priority
            task.priority = 5
            self.assertEqual(task.priority, 5)

            # Change priority from Low to High
            task.priority = 1
            task.priority = 5
            self.assertEqual(task.priority, 5)
        else:
            self.fail("Task not found")

    def test_send_notifications(self):
        # Functionalities 6: Send Notifications for Tasks
        notifications = self.task_manager.get_notifications()
        self.assertGreater(len(notifications), 0, "No notifications found")

    def test_integrate_with_calendar(self):
        # Functionalities 7: Integrate with a Calendar for Task Scheduling
        self.fail("Calendar integration not implemented")

if __name__ == '__main__':
    unittest.main()
