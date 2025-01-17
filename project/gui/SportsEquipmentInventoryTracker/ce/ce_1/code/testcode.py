import unittest
from equipment_manager import EquipmentManager

class TestEquipmentManager(unittest.TestCase):

    def setUp(self):
        self.manager = EquipmentManager()

    def test_add_equipment(self):
        # Functionalities 1: Input Information About Sports Equipment
        new_equipment = {
            "type": "Basketball",
            "quantity": 15,
            "condition": "New",
            "availability": "Available",
            "location": "Storage Room D"
        }
        self.manager.add_equipment(new_equipment)
        self.assertIn(new_equipment, self.manager.data)

    def test_update_equipment(self):
        # Functionalities 2: Update Information About Sports Equipment
        updated_data = {
            "quantity": 12,
            "condition": "Used"
        }
        self.manager.update_equipment(0, updated_data)
        self.assertEqual(self.manager.data[0]['quantity'], 12)
        self.assertEqual(self.manager.data[0]['condition'], "Used")

    def test_track_quantity(self):
        # Functionalities 3: Track the Quantity of Each Equipment Item
        self.assertEqual(self.manager.data[0]['quantity'], 10)

    def test_track_condition(self):
        # Functionalities 4: Track the Condition of Each Equipment Item
        self.assertEqual(self.manager.data[0]['condition'], "New")

    def test_view_availability(self):
        # Functionalities 5: View the Availability of Equipment
        self.assertEqual(self.manager.data[0]['availability'], "Available")

    def test_view_location(self):
        # Functionalities 6: View the Location of Equipment
        self.assertEqual(self.manager.data[0]['location'], "Storage Room A")

    def test_set_alerts(self):
        # Functionalities 7: Set Alerts for Maintenance or Replacement of Equipment
        self.fail("not implemented")

    def test_search_equipment(self):
        # Functionalities 8: Search for Specific Equipment Items
        results = self.manager.search_equipment("Soccer Ball")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['type'], "Soccer Ball")

    def test_filter_equipment(self):
        # Functionalities 9: Filter Equipment Based on Specific Criteria
        criteria = {"availability": "Available"}
        results = self.manager.filter_equipment(criteria)
        self.assertTrue(all(item['availability'] == "Available" for item in results))

if __name__ == '__main__':
    unittest.main()
