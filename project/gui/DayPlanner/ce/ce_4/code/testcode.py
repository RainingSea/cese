import unittest
from main import TaskManager, Task

class TestDayPlanner(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()

    def test_input_daily_tasks(self):
        # Test adding a valid task
        task = Task(3, "Complete project report", 1, "Work", "1:00 PM - 2:00 PM")
        self.task_manager.add_task(task)
        self.assertIn(task, self.task_manager.tasks)

        # Test adding a task with an empty description
        with self.assertRaises(ValueError):
            task = Task(4, "", 1, "Work", "3:00 PM - 4:00 PM")
            self.task_manager.add_task(task)

    def test_set_priorities_for_tasks(self):
        # Test setting a priority for a new task
        task = Task(5, "Prepare for meeting", 2, "Work", "4:00 PM - 5:00 PM")
        self.task_manager.add_task(task)
        self.assertEqual(task.priority, 2)

        # Test changing the priority of an existing task
        task.priority = 3
        self.assertEqual(task.priority, 3)

    def test_categorize_tasks(self):
        # Test categorizing a task correctly
        task = Task(6, "Grocery shopping", 2, "Personal", "5:00 PM - 6:00 PM")
        self.task_manager.add_task(task)
        self.assertEqual(task.category, "Personal")

        # Test categorizing a task with an invalid category
        with self.assertRaises(ValueError):
            task = Task(7, "Invalid task", 2, "InvalidCategory", "6:00 PM - 7:00 PM")
            self.task_manager.add_task(task)

    def test_allocate_specific_time_slots_for_tasks(self):
        # Test allocating a specific time slot
        task = Task(8, "Doctor appointment", 1, "Personal", "3:00 PM - 4:00 PM")
        self.task_manager.add_task(task)
        self.assertEqual(task.time_slot, "3:00 PM - 4:00 PM")

        # Test overlapping time slots
        with self.assertRaises(ValueError):
            task = Task(9, "Another appointment", 1, "Personal", "3:30 PM - 4:30 PM")
            self.task_manager.add_task(task)

    def test_provide_reminders_and_notifications(self):
        # This functionality is not implemented in the codebase
        self.fail("Reminder functionality not implemented")

    def test_offer_visual_overview_of_the_day(self):
        # This functionality is not implemented in the codebase
        self.fail("Visual overview functionality not implemented")

if __name__ == '__main__':
    unittest.main()
