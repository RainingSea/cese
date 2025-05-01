import unittest
import json
import os
from main import InventoryManager

class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        # Create an instance of InventoryManager
        self.manager = InventoryManager()
        # Clear existing data for testing
        self.manager.equipment = []
        self.manager.alerts = []
        self.manager.save_equipment()
        self.manager.save_alerts()

    def test_add_equipment(self):
        # Functionalities 1: Input Information About Sports Equipment
        self.manager.add_equipment("Tennis Racket", 10, "Good", "Storage Room")
        equipment_list = self.manager.get_equipment()
        self.assertEqual(len(equipment_list), 1)
        self.assertEqual(equipment_list[0].name, "Tennis Racket")
        self.assertEqual(equipment_list[0].quantity, 10)
        self.assertEqual(equipment_list[0].condition, "Good")
        self.assertEqual(equipment_list[0].location, "Storage Room")

    def test_update_equipment(self):
        # Functionalities 2: Update Information About Sports Equipment
        self.manager.add_equipment("Soccer Ball", 15, "Fair", "Field")
        self.manager.update_equipment("Soccer Ball", 20, "Good", "Equipment Shed")
        equipment_list = self.manager.get_equipment()
        self.assertEqual(equipment_list[0].quantity, 20)
        self.assertEqual(equipment_list[0].condition, "Good")
        self.assertEqual(equipment_list[0].location, "Equipment Shed")

    def test_track_quantity(self):
        # Functionalities 3: Track the Quantity of Each Equipment Item
        self.manager.add_equipment("Baseball Glove", 5, "Excellent", "Equipment Shed")
        equipment_list = self.manager.get_equipment()
        self.assertEqual(equipment_list[0].quantity, 5)

    def test_track_condition(self):
        # Functionalities 4: Track the Condition of Each Equipment Item
        self.manager.add_equipment("Hockey Stick", 3, "Needs Repair", "Storage Room")
        equipment_list = self.manager.get_equipment()
        self.assertEqual(equipment_list[0].condition, "Needs Repair")

    def test_view_availability(self):
        # Functionalities 5: View the Availability of Equipment
        self.manager.add_equipment("Tennis Racket", 0, "Good", "Storage Room")
        equipment_list = self.manager.get_equipment()
        self.assertEqual(equipment_list[0].quantity, 0)  # Indicating out of stock

    def test_view_location(self):
        # Functionalities 6: View the Location of Equipment
        self.manager.add_equipment("Soccer Ball", 15, "Fair", "Field")
        equipment_list = self.manager.get_equipment()
        self.assertEqual(equipment_list[0].location, "Field")

    def test_set_alert(self):
        # Functionalities 7: Set Alerts for Maintenance or Replacement of Equipment
        self.manager.set_alert("Tennis Racket", "Maintenance")
        alerts_list = self.manager.get_alerts()
        self.assertEqual(len(alerts_list), 1)
        self.assertEqual(alerts_list[0].name, "Tennis Racket")
        self.assertEqual(alerts_list[0].alert_type, "Maintenance")

    def test_search_equipment(self):
        # Functionalities 8: Search for Specific Equipment Items
        self.manager.add_equipment("Baseball Glove", 5, "Excellent", "Equipment Shed")
        equipment_list = self.manager.get_equipment()
        search_result = [item for item in equipment_list if item.name == "Baseball Glove"]
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0].name, "Baseball Glove")

    def test_filter_equipment(self):
        # Functionalities 9: Filter Equipment Based on Specific Criteria
        self.manager.add_equipment("Tennis Racket", 10, "Good", "Storage Room")
        self.manager.add_equipment("Soccer Ball", 15, "Fair", "Field")
        filtered_list = [item for item in self.manager.get_equipment() if item.condition == "Good"]
        self.assertEqual(len(filtered_list), 1)
        self.assertEqual(filtered_list[0].name, "Tennis Racket")

if __name__ == '__main__':
    unittest.main()
