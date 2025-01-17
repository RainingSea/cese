import unittest
from inventory_manager import InventoryManager

class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        # Setup a test instance of InventoryManager with a test JSON file
        self.inventory_manager = InventoryManager("test_equipment.json")
        # Clear the test data before each test
        self.inventory_manager.equipment = []
        self.inventory_manager.save_data()

    def test_input_information_about_sports_equipment(self):
        # Functionalities 1: Input Information About Sports Equipment
        self.inventory_manager.add_equipment("Tennis Racket", 5, "Good", "Storage Room")
        self.assertEqual(len(self.inventory_manager.equipment), 1)
        self.assertEqual(self.inventory_manager.equipment[0]['name'], "Tennis Racket")
        self.assertEqual(self.inventory_manager.equipment[0]['quantity'], 5)
        self.assertEqual(self.inventory_manager.equipment[0]['condition'], "Good")
        self.assertEqual(self.inventory_manager.equipment[0]['location'], "Storage Room")

    def test_update_information_about_sports_equipment(self):
        # Functionalities 2: Update Information About Sports Equipment
        self.inventory_manager.add_equipment("Soccer Ball", 10, "Fair", "Main Hall")
        self.inventory_manager.update_equipment("Soccer Ball", 12, "Good", "Gym")
        self.assertEqual(self.inventory_manager.equipment[0]['quantity'], 12)
        self.assertEqual(self.inventory_manager.equipment[0]['condition'], "Good")
        self.assertEqual(self.inventory_manager.equipment[0]['location'], "Gym")

    def test_track_quantity_of_each_equipment_item(self):
        # Functionalities 3: Track the Quantity of Each Equipment Item
        self.inventory_manager.add_equipment("Basketball", 8, "Excellent", "Gym")
        self.assertEqual(self.inventory_manager.equipment[0]['quantity'], 8)

    def test_track_condition_of_each_equipment_item(self):
        # Functionalities 4: Track the Condition of Each Equipment Item
        self.inventory_manager.add_equipment("Basketball", 8, "Excellent", "Gym")
        self.assertEqual(self.inventory_manager.equipment[0]['condition'], "Excellent")

    def test_view_availability_of_equipment(self):
        # Functionalities 5: View the Availability of Equipment
        # This functionality is not implemented in the codebase
        self.fail("not implemented")

    def test_view_location_of_equipment(self):
        # Functionalities 6: View the Location of Equipment
        self.inventory_manager.add_equipment("Basketball", 8, "Excellent", "Gym")
        self.assertEqual(self.inventory_manager.equipment[0]['location'], "Gym")

    def test_set_alerts_for_maintenance_or_replacement(self):
        # Functionalities 7: Set Alerts for Maintenance or Replacement of Equipment
        # This functionality is not implemented in the codebase
        self.fail("not implemented")

    def test_search_for_specific_equipment_items(self):
        # Functionalities 8: Search for Specific Equipment Items
        self.inventory_manager.add_equipment("Tennis Racket", 5, "Good", "Storage Room")
        results = self.inventory_manager.search_equipment("Tennis")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Tennis Racket")

    def test_filter_equipment_based_on_specific_criteria(self):
        # Functionalities 9: Filter Equipment Based on Specific Criteria
        self.inventory_manager.add_equipment("Tennis Racket", 5, "Good", "Storage Room")
        self.inventory_manager.add_equipment("Soccer Ball", 10, "Fair", "Main Hall")
        filtered_results = self.inventory_manager.filter_equipment("Good", "Storage Room")
        self.assertEqual(len(filtered_results), 1)
        self.assertEqual(filtered_results[0]['name'], "Tennis Racket")

if __name__ == '__main__':
    unittest.main()
