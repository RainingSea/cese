import unittest
from inventory_manager import InventoryManager

class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        self.manager = InventoryManager()

    def test_add_equipment(self):
        # Functionalities 1: Input Information About Sports Equipment
        initial_count = len(self.manager.equipment_list)
        self.manager.add_equipment("Volleyball", "Ball", 12, "New", "Storage Room C")
        self.assertEqual(len(self.manager.equipment_list), initial_count + 1)
        self.assertEqual(self.manager.equipment_list[-1].name, "Volleyball")

    def test_update_equipment(self):
        # Functionalities 2: Update Information About Sports Equipment
        self.manager.add_equipment("Volleyball", "Ball", 12, "New", "Storage Room C")
        self.manager.update_equipment("Volleyball", 15, "Used", "Storage Room D")
        equipment = self.manager.search_equipment("Volleyball")[0]
        self.assertEqual(equipment.quantity, 15)
        self.assertEqual(equipment.condition, "Used")
        self.assertEqual(equipment.location, "Storage Room D")

    def test_track_quantity(self):
        # Functionalities 3: Track the Quantity of Each Equipment Item
        equipment = self.manager.search_equipment("Basketball")[0]
        self.assertEqual(equipment.quantity, 10)

    def test_track_condition(self):
        # Functionalities 4: Track the Condition of Each Equipment Item
        equipment = self.manager.search_equipment("Tennis Racket")[0]
        self.assertEqual(equipment.condition, "Used")

    def test_view_availability(self):
        # Functionalities 5: View the Availability of Equipment
        equipment = self.manager.search_equipment("Soccer Ball")[0]
        self.assertTrue(equipment.availability)

    def test_view_location(self):
        # Functionalities 6: View the Location of Equipment
        equipment = self.manager.search_equipment("Basketball")[0]
        self.assertEqual(equipment.location, "Storage Room A")

    def test_set_alerts(self):
        # Functionalities 7: Set Alerts for Maintenance or Replacement of Equipment
        self.fail("not implemented")

    def test_search_equipment(self):
        # Functionalities 8: Search for Specific Equipment Items
        results = self.manager.search_equipment("Soccer")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Soccer Ball")

    def test_filter_equipment(self):
        # Functionalities 9: Filter Equipment Based on Specific Criteria
        criteria = {"type": "Ball", "condition": "New"}
        results = self.manager.filter_equipment(criteria)
        self.assertEqual(len(results), 2)
        self.assertTrue(all(equipment.type == "Ball" and equipment.condition == "New" for equipment in results))

if __name__ == '__main__':
    unittest.main()
