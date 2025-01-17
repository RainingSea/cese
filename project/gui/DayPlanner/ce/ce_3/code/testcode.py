import unittest
from task_manager import TaskManager
from task import Task
from reminder import Reminder

class TestDayPlanner(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()
        self.reminder = Reminder()

    def test_input_daily_tasks(self):
        # Test adding a valid task
        task = Task("Complete project report", 1, "Work", "09:00-10:00")
        self.task_manager.add_task(task)
        self.assertIn(task, self.task_manager.tasks)

        # Test adding a task with an empty description
        with self.assertRaises(ValueError):
            task = Task("", 1, "Work", "09:00-10:00")
            self.task_manager.add_task(task)

    def test_set_priorities_for_tasks(self):
        # Add a task and set priority
        task = Task("Prepare for meeting", 2, "Work", "10:00-11:00")
        self.task_manager.add_task(task)
        self.assertEqual(task.priority, 2)

        # Change the priority of an existing task
        task.priority = 3
        self.assertEqual(task.priority, 3)

    def test_categorize_tasks(self):
        # Add a task and categorize it
        task = Task("Grocery shopping", 1, "Personal", "11:00-12:00")
        self.task_manager.add_task(task)
        self.assertEqual(task.category, "Personal")

        # Attempt to categorize a task with an invalid category
        with self.assertRaises(ValueError):
            task = Task("Invalid task", 1, "InvalidCategory", "12:00-13:00")
            self.task_manager.add_task(task)

    def test_allocate_specific_time_slots_for_tasks(self):
        # Add a task with a specific time slot
        task = Task("Doctor appointment", 1, "Health", "15:00-16:00")
        self.task_manager.add_task(task)
        self.assertEqual(task.time_slot, "15:00-16:00")

        # Attempt to allocate a time slot that overlaps with an existing task
        with self.assertRaises(ValueError):
            task = Task("Overlapping task", 1, "Work", "15:30-16:30")
            self.task_manager.add_task(task)

    def test_provide_reminders_and_notifications(self):
        # Add a task and set a reminder
        self.reminder.add_reminder("Submit assignment reminder")
        self.assertIn("Submit assignment reminder", self.reminder.reminders)

        # Check reminders section
        self.assertEqual(len(self.reminder.reminders), 1)

    def test_offer_a_visual_overview_of_the_day(self):
        # Add multiple tasks
        tasks = [
            Task("Team meeting", 1, "Work", "09:00-10:00"),
            Task("Lunch with friend", 1, "Personal", "12:00-13:00"),
            Task("Gym", 1, "Health", "18:00-19:00")
        ]
        for task in tasks:
            self.task_manager.add_task(task)

        # Check if tasks are added correctly
        self.assertEqual(len(self.task_manager.tasks), 3)

        # Refresh overview (simulated by reloading tasks)
        self.task_manager.load_tasks()
        self.assertEqual(len(self.task_manager.tasks), 3)

if __name__ == '__main__':
    unittest.main()
