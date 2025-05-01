import unittest
import json
import os
from main import Equipment, Inventory, Main

class TestSportsEquipmentInventoryTracker(unittest.TestCase):

    def setUp(self):
        # Create a temporary inventory for testing
        self.inventory = Inventory()
        self.test_equipment = Equipment("Test Racket", "Racket", 5, "Good", True, "Test Room")
        self.inventory.add_equipment(self.test_equipment)

    def tearDown(self):
        # Clean up the equipment.json file after tests
        if os.path.exists('equipment.json'):
            os.remove('equipment.json')

    def test_add_equipment(self):
        # Functionalities 1: Input Information About Sports Equipment
        self.assertEqual(len(self.inventory.equipment_list), 1)
        self.assertEqual(self.inventory.equipment_list[0].name, "Test Racket")

    def test_update_equipment(self):
        # Functionalities 2: Update Information About Sports Equipment
        updated_equipment = Equipment("Test Racket", "Racket", 10, "Needs Repair", True, "Test Room")
        self.inventory.update_equipment(updated_equipment)
        self.assertEqual(self.inventory.equipment_list[0].quantity, 10)
        self.assertEqual(self.inventory.equipment_list[0].condition, "Needs Repair")

    def test_track_quantity(self):
        # Functionalities 3: Track the Quantity of Each Equipment Item
        quantity = self.inventory.equipment_list[0].quantity
        self.assertEqual(quantity, 5)

    def test_track_condition(self):
        # Functionalities 4: Track the Condition of Each Equipment Item
        condition = self.inventory.equipment_list[0].condition
        self.assertEqual(condition, "Good")

    def test_view_availability(self):
        # Functionalities 5: View the Availability of Equipment
        availability = self.inventory.equipment_list[0].availability
        self.assertTrue(availability)

    def test_view_location(self):
        # Functionalities 6: View the Location of Equipment
        location = self.inventory.equipment_list[0].location
        self.assertEqual(location, "Test Room")

    def test_set_alerts(self):
        # Functionalities 7: Set Alerts for Maintenance or Replacement of Equipment
        self.fail("not implemented")  # Alert functionality is not implemented in the codebase

    def test_search_equipment(self):
        # Functionalities 8: Search for Specific Equipment Items
        results = self.inventory.search_equipment("Test Racket")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Test Racket")

    def test_filter_equipment(self):
        # Functionalities 9: Filter Equipment Based on Specific Criteria
        criteria = {"type": "Racket", "availability": True}
        results = self.inventory.filter_equipment(criteria)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Test Racket")

if __name__ == '__main__':
    unittest.main()
