import unittest
from main import Main
from task_manager import TaskManager

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()
        self.task_manager.load_data()  # Load existing tasks and members for testing

    def test_create_task(self):
        # Functionalities 1: Create Tasks
        initial_task_count = len(self.task_manager.tasks)
        self.task_manager.create_task("Prepare Report", "Compile monthly sales data", "2023-12-10", "High")
        self.assertEqual(len(self.task_manager.tasks), initial_task_count + 1)
        self.assertEqual(self.task_manager.tasks[-1]['title'], "Prepare Report")

    def test_assign_task(self):
        # Functionalities 2: Assign Tasks to Team Members
        self.task_manager.members.append("John Doe")  # Add a member for testing
        self.task_manager.create_task("Prepare Report", "Compile monthly sales data", "2023-12-10", "High")
        self.task_manager.assign_task(0, 0)  # Assign the first task to the first member
        self.assertEqual(self.task_manager.tasks[0]['assigned_to'], "John Doe")

    def test_set_deadline(self):
        # Functionalities 3: Set Deadlines for Tasks
        self.task_manager.create_task("Prepare Report", "Compile monthly sales data", "2023-12-10", "High")
        self.assertEqual(self.task_manager.tasks[-1]['deadline'], "2023-12-10")

    def test_track_task_progress(self):
        # Functionalities 4: Track Task Progress
        self.task_manager.create_task("Prepare Report", "Compile monthly sales data", "2023-12-10", "High")
        self.task_manager.update_progress(0, "50%")
        self.assertEqual(self.task_manager.tasks[0]['status'], "50%")
        self.task_manager.update_progress(0, "Completed")
        self.assertEqual(self.task_manager.tasks[0]['status'], "Completed")

    def test_prioritize_tasks(self):
        # Functionalities 5: Prioritize Tasks
        self.task_manager.create_task("Prepare Report", "Compile monthly sales data", "2023-12-10", "Low")
        self.task_manager.tasks[-1]['priority'] = "High"
        self.assertEqual(self.task_manager.tasks[-1]['priority'], "High")

    def test_send_notifications(self):
        # Functionalities 6: Send Notifications for Tasks
        self.task_manager.create_task("Prepare Report", "Compile monthly sales data", "2023-12-10", "High")
        self.task_manager.send_notification("Task 'Prepare Report' is due soon.")
        self.assertIn("Task 'Prepare Report' is due soon.", self.task_manager.notifications)

    def test_calendar_integration(self):
        # Functionalities 7: Integrate with a Calendar for Task Scheduling
        self.fail("Calendar integration not implemented")

if __name__ == '__main__':
    unittest.main()
