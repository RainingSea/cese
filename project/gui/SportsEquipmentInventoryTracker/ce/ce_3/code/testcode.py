import unittest
from inventory_manager import InventoryManager
from equipment import Equipment

class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        self.manager = InventoryManager()

    def test_input_information_about_sports_equipment(self):
        # Functionalities 1: Input Information About Sports Equipment
        new_equipment = Equipment("3", "Basketball", "Ball", 20, "Good", "Storage Room C", "Inflate every week")
        self.manager.add_equipment(new_equipment)
        self.assertIn(new_equipment, self.manager.equipment_list)

    def test_update_information_about_sports_equipment(self):
        # Functionalities 2: Update Information About Sports Equipment
        equipment_to_update = self.manager.equipment_list[0]
        equipment_to_update.quantity = 12
        self.manager.update_equipment(equipment_to_update)
        updated_equipment = self.manager.equipment_list[0]
        self.assertEqual(updated_equipment.quantity, 12)

    def test_track_quantity_of_each_equipment_item(self):
        # Functionalities 3: Track the Quantity of Each Equipment Item
        equipment = self.manager.equipment_list[0]
        self.assertEqual(equipment.quantity, 10)

    def test_track_condition_of_each_equipment_item(self):
        # Functionalities 4: Track the Condition of Each Equipment Item
        equipment = self.manager.equipment_list[0]
        self.assertEqual(equipment.condition, "Good")

    def test_view_availability_of_equipment(self):
        # Functionalities 5: View the Availability of Equipment
        # This functionality is not implemented in the codebase
        self.fail("View availability of equipment functionality not implemented")

    def test_view_location_of_equipment(self):
        # Functionalities 6: View the Location of Equipment
        equipment = self.manager.equipment_list[0]
        self.assertEqual(equipment.location, "Storage Room A")

    def test_set_alerts_for_maintenance_or_replacement_of_equipment(self):
        # Functionalities 7: Set Alerts for Maintenance or Replacement of Equipment
        equipment = self.manager.equipment_list[0]
        self.assertEqual(equipment.maintenance_alert, "Check strings every 6 months")

    def test_search_for_specific_equipment_items(self):
        # Functionalities 8: Search for Specific Equipment Items
        results = self.manager.search_equipment("Tennis Racket")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Tennis Racket")

    def test_filter_equipment_based_on_specific_criteria(self):
        # Functionalities 9: Filter Equipment Based on Specific Criteria
        criteria = {"type": "Ball"}
        filtered_results = self.manager.filter_equipment(criteria)
        self.assertEqual(len(filtered_results), 1)
        self.assertEqual(filtered_results[0].name, "Soccer Ball")

if __name__ == '__main__':
    unittest.main()
