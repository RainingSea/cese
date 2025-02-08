import unittest
from TaskManager import TaskManager, Task
from Notification import Notification
from CalendarIntegration import CalendarIntegration
import datetime

class TestTaskApp(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()
        self.notification = Notification()
        self.calendar_integration = CalendarIntegration()

    def test_create_task(self):
        # Functionalities 1: Create Tasks
        initial_task_count = len(self.task_manager.get_tasks())
        self.task_manager.create_task("Prepare Report", "Compile monthly sales data", 3, "John Doe", "2023-12-01")
        self.assertEqual(len(self.task_manager.get_tasks()), initial_task_count + 1)
        self.assertEqual(self.task_manager.get_tasks()[-1].title, "Prepare Report")

    def test_assign_task_to_member(self):
        # Functionalities 2: Assign Tasks to Team Members
        self.task_manager.create_task("Prepare Report", "Compile monthly sales data", 3, "John Doe", "2023-12-01")
        task = self.task_manager.get_tasks()[-1]
        self.assertEqual(task.assigned_member, "John Doe")

    def test_set_deadline_for_task(self):
        # Functionalities 3: Set Deadlines for Tasks
        self.task_manager.create_task("Prepare Report", "Compile monthly sales data", 3, "John Doe", "2023-12-01")
        task = self.task_manager.get_tasks()[-1]
        self.assertEqual(task.deadline, "2023-12-01")

    def test_track_task_progress(self):
        # Functionalities 4: Track Task Progress
        self.task_manager.create_task("Prepare Report", "Compile monthly sales data", 3, "John Doe", "2023-12-01")
        task = self.task_manager.get_tasks()[-1]
        self.task_manager.update_task_status(task.title, "Completed")
        self.assertEqual(task.status, "Completed")

    def test_prioritize_tasks(self):
        # Functionalities 5: Prioritize Tasks
        self.task_manager.create_task("Prepare Report", "Compile monthly sales data", 5, "John Doe", "2023-12-01")
        task = self.task_manager.get_tasks()[-1]
        self.assertEqual(task.priority, 5)

    def test_send_notifications_for_tasks(self):
        # Functionalities 6: Send Notifications for Tasks
        self.task_manager.create_task("Prepare Report", "Compile monthly sales data", 3, "John Doe", "2023-12-01")
        task = self.task_manager.get_tasks()[-1]
        self.notification.send_notification(task)
        # Since this is a print statement, we can't directly test it without capturing stdout

    def test_integrate_with_calendar(self):
        # Functionalities 7: Integrate with a Calendar for Task Scheduling
        self.calendar_integration.show_calendar()
        self.calendar_integration.add_task_to_calendar(Task("Prepare Report", "Compile monthly sales data", 3, "John Doe", "2023-12-01", "Pending"))
        # Since this is a print statement, we can't directly test it without capturing stdout

if __name__ == '__main__':
    unittest.main()
