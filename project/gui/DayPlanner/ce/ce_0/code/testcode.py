import unittest
import os
from tkinter import Tk
from main import Main
from task_manager import TaskManager, Task

class TestDayPlanner(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.app = Main(self.root)
        self.task_manager = self.app.task_manager

    def tearDown(self):
        self.root.destroy()
        # Clean up tasks.txt after tests
        if os.path.exists('tasks.txt'):
            os.remove('tasks.txt')

    def test_input_daily_tasks(self):
        # Functionality 1: Input Daily Tasks
        self.app.task_title.insert(0, "Complete project report")
        self.app.priority_var.set("High")
        self.app.category_var.set("Work")
        self.app.time_slot.insert(0, "10:00 AM")
        self.app.add_task()
        self.assertEqual(len(self.task_manager.get_tasks()), 1)
        
        # Test empty task description
        self.app.task_title.delete(0, 'end')
        self.app.add_task()
        self.assertEqual(len(self.task_manager.get_tasks()), 1)  # Should still be 1

    def test_set_priorities_for_tasks(self):
        # Functionality 2: Set Priorities for Tasks
        self.app.task_title.insert(0, "Prepare for meeting")
        self.app.priority_var.set("High")
        self.app.category_var.set("Work")
        self.app.time_slot.insert(0, "11:00 AM")
        self.app.add_task()
        
        self.assertEqual(self.task_manager.get_tasks()[0].priority, "High")
        
        # Change priority
        self.app.task_manager.tasks[0].priority = "Medium"
        self.app.update_task_list()
        self.assertEqual(self.task_manager.get_tasks()[0].priority, "Medium")

    def test_categorize_tasks(self):
        # Functionality 3: Categorize Tasks
        self.app.task_title.insert(0, "Grocery shopping")
        self.app.priority_var.set("Low")
        self.app.category_var.set("Personal")
        self.app.time_slot.insert(0, "12:00 PM")
        self.app.add_task()
        
        self.assertEqual(self.task_manager.get_tasks()[0].category, "Personal")
        
        # Test invalid category
        self.app.category_var.set("InvalidCategory")
        self.app.add_task()
        self.assertEqual(len(self.task_manager.get_tasks()), 1)  # Should still be 1

    def test_allocate_specific_time_slots_for_tasks(self):
        # Functionality 4: Allocate Specific Time Slots for Tasks
        self.app.task_title.insert(0, "Doctor appointment")
        self.app.priority_var.set("High")
        self.app.category_var.set("Personal")
        self.app.time_slot.insert(0, "3:00 PM")
        self.app.add_task()
        
        self.assertEqual(self.task_manager.get_tasks()[0].time_slot, "3:00 PM")
        
        # Test overlapping time slot
        self.app.task_title.insert(0, "Another appointment")
        self.app.time_slot.delete(0, 'end')
        self.app.time_slot.insert(0, "3:00 PM")  # Overlapping time
        self.app.add_task()
        self.assertEqual(len(self.task_manager.get_tasks()), 1)  # Should still be 1

    def test_provide_reminders_and_notifications(self):
        # Functionality 5: Provide Reminders and Notifications
        self.fail("not implemented")  # Reminder functionality not implemented in the codebase

    def test_offer_visual_overview_of_the_day(self):
        # Functionality 6: Offer a Visual Overview of the Day
        self.app.task_title.insert(0, "Team meeting")
        self.app.priority_var.set("Medium")
        self.app.category_var.set("Work")
        self.app.time_slot.insert(0, "1:00 PM")
        self.app.add_task()
        
        self.app.task_title.insert(0, "Lunch with friend")
        self.app.priority_var.set("Low")
        self.app.category_var.set("Personal")
        self.app.time_slot.insert(0, "2:00 PM")
        self.app.add_task()
        
        self.assertEqual(len(self.task_manager.get_tasks()), 2)
        self.app.update_task_list()
        self.assertIn("Team meeting", self.app.task_list.get(0))
        self.assertIn("Lunch with friend", self.app.task_list.get(1))

if __name__ == '__main__':
    unittest.main()
