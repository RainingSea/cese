import unittest
import os
from main import Inventory

class TestSportsEquipmentInventoryTracker(unittest.TestCase):

    def setUp(self):
        self.inventory = Inventory()
        # Clear the equipment list for testing
        self.inventory.equipment_list = []
        self.inventory.save_data()

    def test_add_equipment(self):
        # Functionalities 1: Input Information About Sports Equipment
        self.inventory.add_equipment("Tennis Racket", "Racket", 5, "Good", "Storage Room")
        self.assertEqual(len(self.inventory.equipment_list), 1)
        self.assertEqual(self.inventory.equipment_list[0].name, "Tennis Racket")

    def test_update_equipment(self):
        # Functionalities 2: Update Information About Sports Equipment
        self.inventory.add_equipment("Soccer Ball", "Ball", 10, "Fair", "Equipment Shed")
        self.inventory.update_equipment(0, "Soccer Ball", "Ball", 8, "Good", "Equipment Shed")
        self.assertEqual(self.inventory.equipment_list[0].quantity, 8)
        self.assertEqual(self.inventory.equipment_list[0].condition, "Good")

    def test_track_quantity(self):
        # Functionalities 3: Track the Quantity of Each Equipment Item
        self.inventory.add_equipment("Baseball Bat", "Bat", 3, "Excellent", "Locker Room")
        self.assertEqual(self.inventory.equipment_list[0].quantity, 3)

    def test_track_condition(self):
        # Functionalities 4: Track the Condition of Each Equipment Item
        self.inventory.add_equipment("Tennis Racket", "Racket", 5, "Good", "Storage Room")
        self.assertEqual(self.inventory.equipment_list[0].condition, "Good")

    def test_view_availability(self):
        # Functionalities 5: View the Availability of Equipment
        self.fail("not implemented")  # Availability logic not implemented

    def test_view_location(self):
        # Functionalities 6: View the Location of Equipment
        self.inventory.add_equipment("Soccer Ball", "Ball", 10, "Fair", "Equipment Shed")
        self.assertEqual(self.inventory.equipment_list[0].location, "Equipment Shed")

    def test_set_alerts(self):
        # Functionalities 7: Set Alerts for Maintenance or Replacement of Equipment
        self.fail("not implemented")  # Alert logic not implemented

    def test_search_equipment(self):
        # Functionalities 8: Search for Specific Equipment Items
        self.inventory.add_equipment("Tennis Racket", "Racket", 5, "Good", "Storage Room")
        results = self.inventory.search_equipment("Tennis")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Tennis Racket")

    def test_filter_equipment(self):
        # Functionalities 9: Filter Equipment Based on Specific Criteria
        self.inventory.add_equipment("Tennis Racket", "Racket", 5, "Good", "Storage Room")
        self.inventory.add_equipment("Soccer Ball", "Ball", 10, "Fair", "Equipment Shed")
        results = self.inventory.filter_equipment("Racket", "Good")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Tennis Racket")

if __name__ == '__main__':
    unittest.main()
