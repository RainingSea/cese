import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import subprocess

class TestSportsEquipmentTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        # Initialize the webdriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8109/login')
        time.sleep(2)  # Wait for the page to load

    def tearDown(self):
        # Close the webdriver and stop the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_1_user_registration(self):
        """Test user registration functionality"""
        # Navigate to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        
        # Test case 1: Registration form is displayed
        self.assertIsNotNone(self.driver.find_element(By.ID, 'username'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'password'))
        
        # Test case 2: Successful registration
        username = "testuser"
        password = "testpass123"
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)
        
        # Test case 3: Attempt to register existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'username').send_keys("admin")
        self.driver.find_element(By.ID, 'password').send_keys("anypassword")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        self.assertIn("Registration failed", self.driver.page_source)

    def test_2_user_login(self):
        """Test user login functionality"""
        # Test case 1: Login form is displayed
        self.assertIsNotNone(self.driver.find_element(By.ID, 'username'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'password'))
        
        # Test case 2: Successful login
        self.login("admin", "admin123")
        self.assertIn("Equipment Management", self.driver.page_source)
        
        # Logout for next test
        self.driver.find_element(By.CLASS_NAME, 'logout-btn').click()
        time.sleep(1)
        
        # Test case 3: Invalid login
        self.driver.find_element(By.ID, 'username').send_keys("wronguser")
        self.driver.find_element(By.ID, 'password').send_keys("wrongpass")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)
        self.assertIn("Login failed", self.driver.page_source)

    def test_3_equipment_management(self):
        """Test equipment management functionality"""
        self.login("admin", "admin123")
        
        # Test case 1: Equipment management interface is displayed
        self.assertIn("Add New Equipment", self.driver.page_source)
        self.assertIn("Equipment List", self.driver.page_source)
        
        # Test case 2: Add new equipment
        self.driver.find_element(By.ID, 'name').send_keys("Test Equipment")
        self.driver.find_element(By.ID, 'type').send_keys("Test Type")
        self.driver.find_element(By.ID, 'quantity').send_keys("5")
        Select(self.driver.find_element(By.ID, 'condition')).select_by_visible_text("Good")
        self.driver.find_element(By.ID, 'location').send_keys("Test Location")
        self.driver.find_element(By.ID, 'last_maintenance_date').send_keys("2023-01-01")
        self.driver.find_element(By.XPATH, '//form[@action="/add_equipment"]//button').click()
        time.sleep(1)
        self.assertIn("Test Equipment", self.driver.page_source)
        
        # Test case 3: Update equipment (not implemented in codebase)
        # This would normally involve finding the edit button for an equipment item,
        # making changes, and verifying the update
        # Since it's not implemented, we'll mark this as a failure
        self.fail("Update equipment functionality not implemented in codebase")

    def test_4_view_equipment_details(self):
        """Test viewing equipment details"""
        self.login("admin", "admin123")
        
        # Test case 1: Equipment list is displayed
        equipment_table = self.driver.find_element(By.TAG_NAME, 'table')
        self.assertIsNotNone(equipment_table)
        
        # Test case 2: Equipment details are visible in the table
        # Check that details from equipment.txt are displayed
        self.assertIn("Drill", self.driver.page_source)
        self.assertIn("Power Tool", self.driver.page_source)
        self.assertIn("5", self.driver.page_source)
        self.assertIn("Good", self.driver.page_source)
        self.assertIn("Warehouse A", self.driver.page_source)
        self.assertIn("2023-01-15", self.driver.page_source)

    def test_5_set_alerts(self):
        """Test setting alerts for equipment"""
        self.login("admin", "admin123")
        
        # Test case 1: Set a maintenance alert
        self.driver.find_element(By.ID, 'equipment_name').send_keys("Drill")
        Select(self.driver.find_element(By.ID, 'alert_type')).select_by_visible_text("Maintenance Due")
        self.driver.find_element(By.ID, 'threshold_date').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//form[@action="/set_alert"]//button').click()
        time.sleep(1)
        
        # Test case 2: Check alerts section
        alerts_section = self.driver.find_element(By.XPATH, '//h3[text()="Your Alerts"]/following-sibling::ul')
        self.assertIsNotNone(alerts_section)
        self.assertIn("Drill", alerts_section.text)
        self.assertIn("maintenance", alerts_section.text)
        self.assertIn("2023-12-31", alerts_section.text)

    def test_6_search_equipment(self):
        """Test searching for equipment"""
        self.login("admin", "admin123")
        
        # Test case 1: Search by name
        search_input = self.driver.find_element(By.NAME, 'query')
        search_input.send_keys("Hammer")
        self.driver.find_element(By.XPATH, '//form[@action="/search_equipment"]//button').click()
        time.sleep(1)
        
        equipment_table = self.driver.find_element(By.TAG_NAME, 'table')
        rows = equipment_table.find_elements(By.TAG_NAME, 'tr')
        # Should have header row + 1 data row
        self.assertEqual(len(rows), 2)
        self.assertIn("Hammer", equipment_table.text)
        self.assertNotIn("Drill", equipment_table.text)

    def test_7_filter_equipment(self):
        """Test filtering equipment list"""
        self.login("admin", "admin123")
        
        # Test case 1: Filter by condition
        Select(self.driver.find_element(By.NAME, 'condition')).select_by_visible_text("Worn")
        self.driver.find_element(By.XPATH, '//form[@action="/filter_equipment"]//button').click()
        time.sleep(1)
        
        equipment_table = self.driver.find_element(By.TAG_NAME, 'table')
        self.assertIn("Hammer", equipment_table.text)
        self.assertNotIn("Drill", equipment_table.text)
        
        # Test case 2: Clear filter (not implemented in UI)
        # This would normally involve clicking a "Clear" button
        # Since it's not implemented, we'll refresh the page instead
        self.driver.refresh()
        time.sleep(1)
        equipment_table = self.driver.find_element(By.TAG_NAME, 'table')
        self.assertIn("Drill", equipment_table.text)
        self.assertIn("Hammer", equipment_table.text)

    def test_8_user_logout(self):
        """Test user logout functionality"""
        self.login("admin", "admin123")
        
        # Test case 1: Logout
        self.driver.find_element(By.CLASS_NAME, 'logout-btn').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)
        
        # Test case 2: Attempt to access dashboard after logout
        self.driver.get('http://localhost:8109/dashboard')
        time.sleep(1)
        self.assertIn("Login", self.driver.title)

    def test_9_data_persistence(self):
        """Test data persistence"""
        self.login("admin", "admin123")
        
        # Test case 1: Add new equipment
        self.driver.find_element(By.ID, 'name').send_keys("Persistence Test")
        self.driver.find_element(By.ID, 'type').send_keys("Test Type")
        self.driver.find_element(By.ID, 'quantity').send_keys("10")
        Select(self.driver.find_element(By.ID, 'condition')).select_by_visible_text("New")
        self.driver.find_element(By.ID, 'location').send_keys("Test Location")
        self.driver.find_element(By.ID, 'last_maintenance_date').send_keys("2023-01-01")
        self.driver.find_element(By.XPATH, '//form[@action="/add_equipment"]//button').click()
        time.sleep(1)
        
        # Logout and close
        self.driver.find_element(By.CLASS_NAME, 'logout-btn').click()
        time.sleep(1)
        self.driver.quit()
        self.process.terminate()
        
        # Restart application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8109/login')
        time.sleep(2)
        
        # Login again
        self.login("admin", "admin123")
        
        # Verify equipment is still there
        self.assertIn("Persistence Test", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
