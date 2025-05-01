import unittest
from tkinter import Tk
from main import Main
from task_manager import TaskManager

class TestDayPlanner(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.app = Main(self.root)
        self.task_manager = self.app.task_manager

    def test_input_daily_tasks(self):
        # Functionality 1: Input Daily Tasks
        # Step: Add a valid task
        self.app.task_description.insert(0, "Complete project report")
        self.app.priority_var.set(3)
        self.app.category_var.set("Work")
        self.app.time_slot_entry.insert(0, "10:00 AM")
        self.app.add_task()
        self.assertEqual(len(self.task_manager.get_tasks()), 1)

        # Step: Attempt to input a task with an empty description
        self.app.task_description.delete(0, 'end')
        self.app.add_task()
        self.assertEqual(len(self.task_manager.get_tasks()), 1)  # Should still be 1

    def test_set_priorities_for_tasks(self):
        # Functionality 2: Set Priorities for Tasks
        self.app.task_description.insert(0, "Prepare for meeting")
        self.app.priority_var.set(1)  # High priority
        self.app.category_var.set("Work")
        self.app.time_slot_entry.insert(0, "11:00 AM")
        self.app.add_task()
        self.assertEqual(self.task_manager.get_tasks()[0].priority, 1)

        # Change priority
        self.app.task_manager.tasks[0].priority = 2  # Change to Medium
        self.assertEqual(self.task_manager.get_tasks()[0].priority, 2)

    def test_categorize_tasks(self):
        # Functionality 3: Categorize Tasks
        self.app.task_description.insert(0, "Grocery shopping")
        self.app.priority_var.set(3)
        self.app.category_var.set("Personal")
        self.app.time_slot_entry.insert(0, "5:00 PM")
        self.app.add_task()
        self.assertEqual(self.task_manager.get_tasks()[0].category, "Personal")

        # Attempt to categorize a task with an invalid category
        self.fail("not implemented")  # Placeholder for invalid category test

    def test_allocate_specific_time_slots_for_tasks(self):
        # Functionality 4: Allocate Specific Time Slots for Tasks
        self.app.task_description.insert(0, "Doctor appointment")
        self.app.priority_var.set(2)
        self.app.category_var.set("Personal")
        self.app.time_slot_entry.insert(0, "3:00 PM")
        self.app.add_task()
        self.assertEqual(self.task_manager.get_tasks()[0].time_slot, "3:00 PM")

        # Attempt to allocate a time slot that overlaps with an existing task
        self.fail("not implemented")  # Placeholder for overlapping time slot test

    def test_provide_reminders_and_notifications(self):
        # Functionality 5: Provide Reminders and Notifications
        self.app.task_description.insert(0, "Submit assignment")
        self.app.priority_var.set(2)
        self.app.category_var.set("Study")
        self.app.time_slot_entry.insert(0, "4:00 PM")
        self.app.add_task()
        self.fail("not implemented")  # Placeholder for reminders test

    def test_offer_visual_overview_of_the_day(self):
        # Functionality 6: Offer a Visual Overview of the Day
        self.app.task_description.insert(0, "Team meeting")
        self.app.priority_var.set(1)
        self.app.category_var.set("Work")
        self.app.time_slot_entry.insert(0, "9:00 AM")
        self.app.add_task()

        self.app.task_description.insert(0, "Lunch with friend")
        self.app.priority_var.set(3)
        self.app.category_var.set("Personal")
        self.app.time_slot_entry.insert(0, "12:00 PM")
        self.app.add_task()

        self.app.task_description.insert(0, "Gym")
        self.app.priority_var.set(2)
        self.app.category_var.set("Personal")
        self.app.time_slot_entry.insert(0, "6:00 PM")
        self.app.add_task()

        self.assertEqual(len(self.task_manager.get_tasks()), 3)

        # Refresh the daily overview
        self.app.update_task_list()
        self.assertEqual(self.app.task_listbox.size(), 3)

if __name__ == '__main__':
    unittest.main()
