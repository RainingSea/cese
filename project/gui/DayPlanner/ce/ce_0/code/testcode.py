import unittest
from day_planner import DayPlanner
from task import Task
from category import Category
from reminder import Reminder

class TestDayPlanner(unittest.TestCase):

    def setUp(self):
        # Setup a fresh DayPlanner instance for each test
        self.day_planner = DayPlanner()

    def test_input_daily_tasks(self):
        # Test adding a valid task
        self.day_planner.add_task("Complete project report", 1, "Work", "3:00 PM - 4:00 PM")
        tasks = self.day_planner.view_tasks()
        self.assertIn(["Complete project report", 1, "Work", "3:00 PM - 4:00 PM"], tasks)

        # Test adding a task with an empty description
        with self.assertRaises(ValueError):
            self.day_planner.add_task("", 1, "Work", "3:00 PM - 4:00 PM")

    def test_set_priorities_for_tasks(self):
        # Add a task and set its priority
        self.day_planner.add_task("Prepare for meeting", 2, "Work", "10:00 AM - 11:00 AM")
        self.day_planner.set_priority(0, 3)  # Change priority to High
        tasks = self.day_planner.view_tasks()
        self.assertEqual(tasks[0][1], 3)

        # Change the priority of an existing task
        self.day_planner.set_priority(0, 2)  # Change priority to Medium
        tasks = self.day_planner.view_tasks()
        self.assertEqual(tasks[0][1], 2)

    def test_categorize_tasks(self):
        # Add a task and categorize it
        self.day_planner.add_task("Grocery shopping", 1, "Shopping", "5:00 PM - 6:00 PM")
        self.day_planner.categorize_task(0, "Personal")
        tasks = self.day_planner.view_tasks()
        self.assertEqual(tasks[0][2], "Personal")

        # Attempt to categorize with an invalid category
        with self.assertRaises(ValueError):
            self.day_planner.categorize_task(0, "InvalidCategory")

    def test_allocate_specific_time_slots_for_tasks(self):
        # Add a task and allocate a time slot
        self.day_planner.add_task("Doctor appointment", 1, "Health", "3:00 PM - 4:00 PM")
        tasks = self.day_planner.view_tasks()
        self.assertEqual(tasks[0][3], "3:00 PM - 4:00 PM")

        # Attempt to allocate a conflicting time slot
        self.day_planner.add_task("Another task", 1, "Work", "3:30 PM - 4:30 PM")
        with self.assertRaises(ValueError):
            self.day_planner.allocate_time(1, "3:00 PM - 4:00 PM")

    def test_provide_reminders_and_notifications(self):
        # Add a task and set a reminder
        self.day_planner.add_task("Submit assignment", 1, "Work", "6:00 PM - 7:00 PM")
        reminder = Reminder(0, "5:00 PM")
        reminder.set_reminder()
        reminders = Reminder.get_reminders()
        self.assertIn(["0", "5:00 PM"], reminders)

        # Check reminders section
        self.day_planner.add_task("Another task", 1, "Work", "8:00 PM - 9:00 PM")
        reminder = Reminder(1, "7:00 PM")
        reminder.set_reminder()
        reminders = Reminder.get_reminders()
        self.assertEqual(len(reminders), 2)

    def test_offer_a_visual_overview_of_the_day(self):
        # Add multiple tasks and check the overview
        self.day_planner.add_task("Team meeting", 1, "Work", "9:00 AM - 10:00 AM")
        self.day_planner.add_task("Lunch with friend", 1, "Personal", "12:00 PM - 1:00 PM")
        self.day_planner.add_task("Gym", 1, "Health", "6:00 PM - 7:00 PM")
        overview = self.day_planner.show_overview()
        self.assertEqual(len(overview), 3)

        # Refresh the overview after adding a new task
        self.day_planner.add_task("New task", 1, "Work", "8:00 PM - 9:00 PM")
        overview = self.day_planner.show_overview()
        self.assertEqual(len(overview), 4)

if __name__ == '__main__':
    unittest.main()
