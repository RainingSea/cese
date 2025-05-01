import unittest
import os
from main import Main
from TaskManager import TaskManager

class TestDayPlanner(unittest.TestCase):

    def setUp(self):
        self.app = Main()
        self.task_manager = self.app.task_manager

    def test_input_daily_tasks(self):
        # Functionality 1: Input Daily Tasks
        # Test adding a valid task
        self.app.task_name_entry.insert(0, "Complete project report")
        self.app.start_time_entry.insert(0, "09:00")
        self.app.end_time_entry.insert(0, "10:00")
        self.app.save_task()
        self.assertIn("Complete project report", self.app.display_area.get("1.0", "end"))

        # Test adding a task with an empty description
        self.app.task_name_entry.delete(0, 'end')
        self.app.save_task()
        self.assertIn("Input Error", self.app.display_area.get("1.0", "end"))

    def test_set_priorities_for_tasks(self):
        # Functionality 2: Set Priorities for Tasks
        self.app.task_name_entry.insert(0, "Prepare for meeting")
        self.app.priority_var.set("High")
        self.app.start_time_entry.insert(0, "10:00")
        self.app.end_time_entry.insert(0, "11:00")
        self.app.save_task()
        self.assertIn("Prepare for meeting | High", self.app.display_area.get("1.0", "end"))

        # Change priority of an existing task
        self.task_manager.tasks[0].priority = "Medium"
        self.app.display_tasks()
        self.assertIn("Prepare for meeting | Medium", self.app.display_area.get("1.0", "end"))

    def test_categorize_tasks(self):
        # Functionality 3: Categorize Tasks
        self.app.task_name_entry.insert(0, "Grocery shopping")
        self.app.category_var.set("Personal")
        self.app.start_time_entry.insert(0, "12:00")
        self.app.end_time_entry.insert(0, "13:00")
        self.app.save_task()
        self.assertIn("Grocery shopping | Personal", self.app.display_area.get("1.0", "end"))

        # Test invalid category
        self.app.category_var.set("InvalidCategory")
        self.app.save_task()
        self.assertIn("Input Error", self.app.display_area.get("1.0", "end"))

    def test_allocate_specific_time_slots_for_tasks(self):
        # Functionality 4: Allocate Specific Time Slots for Tasks
        self.app.task_name_entry.insert(0, "Doctor appointment")
        self.app.start_time_entry.insert(0, "15:00")
        self.app.end_time_entry.insert(0, "16:00")
        self.app.save_task()
        self.assertIn("Doctor appointment | 15:00 - 16:00", self.app.display_area.get("1.0", "end"))

        # Test overlapping time slot
        self.app.start_time_entry.delete(0, 'end')
        self.app.start_time_entry.insert(0, "10:30")
        self.app.end_time_entry.delete(0, 'end')
        self.app.end_time_entry.insert(0, "11:30")
        self.app.save_task()
        self.assertIn("Input Error", self.app.display_area.get("1.0", "end"))

    def test_provide_reminders_and_notifications(self):
        # Functionality 5: Provide Reminders and Notifications
        self.app.task_name_entry.insert(0, "Submit assignment")
        self.app.start_time_entry.insert(0, "14:00")
        self.app.end_time_entry.insert(0, "15:00")
        self.app.save_task()
        # Reminder functionality is not implemented, so we will fail this test
        self.fail("Reminder functionality not implemented")

    def test_offer_visual_overview_of_the_day(self):
        # Functionality 6: Offer a Visual Overview of the Day
        self.app.task_name_entry.insert(0, "Team meeting")
        self.app.start_time_entry.insert(0, "09:00")
        self.app.end_time_entry.insert(0, "10:00")
        self.app.save_task()

        self.app.task_name_entry.insert(0, "Lunch with friend")
        self.app.start_time_entry.insert(0, "12:00")
        self.app.end_time_entry.insert(0, "13:00")
        self.app.save_task()

        self.app.task_name_entry.insert(0, "Gym")
        self.app.start_time_entry.insert(0, "17:00")
        self.app.end_time_entry.insert(0, "18:00")
        self.app.save_task()

        self.assertIn("Team meeting", self.app.display_area.get("1.0", "end"))
        self.assertIn("Lunch with friend", self.app.display_area.get("1.0", "end"))
        self.assertIn("Gym", self.app.display_area.get("1.0", "end"))

        # Refresh the daily overview
        self.app.display_tasks()
        self.assertIn("Team meeting", self.app.display_area.get("1.0", "end"))

if __name__ == '__main__':
    unittest.main()
