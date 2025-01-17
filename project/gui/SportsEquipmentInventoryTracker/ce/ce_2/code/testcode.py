import unittest
from inventory_manager import InventoryManager
from equipment import Equipment

class TestSportsEquipmentInventory(unittest.TestCase):

    def setUp(self):
        # Initialize InventoryManager with a test data file
        self.inventory_manager = InventoryManager('equipment_inventory.json')

    def test_input_information_about_sports_equipment(self):
        # Functionalities 1: Input Information About Sports Equipment
        new_equipment = {
            'name': 'Basketball',
            'type': 'Ball',
            'quantity': 15,
            'condition': 'New',
            'availability': True,
            'location': 'Gym',
            'maintenance_alert': 'Check air pressure weekly'
        }
        self.inventory_manager.add_equipment(new_equipment)
        added_equipment = self.inventory_manager.search_equipment('Basketball')
        self.assertEqual(len(added_equipment), 1)
        self.assertEqual(added_equipment[0].name, 'Basketball')

    def test_update_information_about_sports_equipment(self):
        # Functionalities 2: Update Information About Sports Equipment
        self.inventory_manager.update_equipment('Tennis Racket', {'quantity': 8, 'condition': 'Used'})
        updated_equipment = self.inventory_manager.search_equipment('Tennis Racket')
        self.assertEqual(len(updated_equipment), 1)
        self.assertEqual(updated_equipment[0].quantity, 8)
        self.assertEqual(updated_equipment[0].condition, 'Used')

    def test_track_quantity_of_each_equipment_item(self):
        # Functionalities 3: Track the Quantity of Each Equipment Item
        equipment = self.inventory_manager.search_equipment('Soccer Ball')
        self.assertEqual(len(equipment), 1)
        self.assertEqual(equipment[0].quantity, 5)

    def test_track_condition_of_each_equipment_item(self):
        # Functionalities 4: Track the Condition of Each Equipment Item
        equipment = self.inventory_manager.search_equipment('Baseball Glove')
        self.assertEqual(len(equipment), 1)
        self.assertEqual(equipment[0].condition, 'Used')

    def test_view_availability_of_equipment(self):
        # Functionalities 5: View the Availability of Equipment
        equipment = self.inventory_manager.search_equipment('Soccer Ball')
        self.assertEqual(len(equipment), 1)
        self.assertTrue(equipment[0].availability)

    def test_view_location_of_equipment(self):
        # Functionalities 6: View the Location of Equipment
        equipment = self.inventory_manager.search_equipment('Tennis Racket')
        self.assertEqual(len(equipment), 1)
        self.assertEqual(equipment[0].location, 'Storage Room')

    def test_set_alerts_for_maintenance_or_replacement_of_equipment(self):
        # Functionalities 7: Set Alerts for Maintenance or Replacement of Equipment
        equipment = self.inventory_manager.search_equipment('Soccer Ball')
        self.assertEqual(len(equipment), 1)
        self.assertEqual(equipment[0].maintenance_alert, 'Check for air pressure monthly')

    def test_search_for_specific_equipment_items(self):
        # Functionalities 8: Search for Specific Equipment Items
        search_result = self.inventory_manager.search_equipment('Baseball Glove')
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0].name, 'Baseball Glove')

    def test_filter_equipment_based_on_specific_criteria(self):
        # Functionalities 9: Filter Equipment Based on Specific Criteria
        filtered_result = self.inventory_manager.filter_equipment({'type': 'Ball'})
        self.assertEqual(len(filtered_result), 1)
        self.assertEqual(filtered_result[0].name, 'Soccer Ball')

if __name__ == '__main__':
    unittest.main()
