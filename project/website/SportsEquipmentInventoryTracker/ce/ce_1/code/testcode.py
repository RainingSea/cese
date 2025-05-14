import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import subprocess

class TestSportsEquipmentInventoryTracker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the Flask application
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        # Stop the Flask application
        cls.process.terminate()

    def setUp(self):
        # Initialize the webdriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8110/login')
        time.sleep(1)

    def tearDown(self):
        # Close the webdriver session
        self.driver.quit()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)

    def test_01_user_registration(self):
        """Test user registration functionality"""
        # Navigate to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        
        # Verify registration form is displayed
        self.assertIn("Register", self.driver.title)
        self.assertTrue(self.driver.find_element(By.NAME, 'username').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'password').is_displayed())
        
        # Test successful registration
        username = "testuser_" + str(int(time.time()))
        password = "testpass123"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        
        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)
        
        # Test registration with existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        
        # Verify error message
        error_message = self.driver.find_element(By.CSS_SELECTOR, 'p[style="color:red"]').text
        self.assertEqual(error_message, "Username already exists")

    def test_02_user_login(self):
        """Test user login functionality"""
        # Verify login form is displayed
        self.assertIn("Login", self.driver.title)
        self.assertTrue(self.driver.find_element(By.NAME, 'username').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'password').is_displayed())
        
        # Test successful login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)
        
        # Logout for next test
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        
        # Test failed login
        self.driver.find_element(By.NAME, 'username').send_keys("wronguser")
        self.driver.find_element(By.NAME, 'password').send_keys("wrongpass")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)
        
        # Verify error message
        error_message = self.driver.find_element(By.CSS_SELECTOR, 'p[style="color:red"]').text
        self.assertEqual(error_message, "Invalid credentials")

    def test_03_equipment_management(self):
        """Test equipment management functionality"""
        self.login("admin", "admin123")
        
        # Verify dashboard is displayed
        self.assertIn("Dashboard", self.driver.title)
        self.assertTrue(self.driver.find_element(By.XPATH, '//h2[text()="Add Equipment"]').is_displayed())
        
        # Test adding new equipment
        equipment_name = "Test Equipment " + str(int(time.time()))
        self.driver.find_element(By.NAME, 'name').send_keys(equipment_name)
        self.driver.find_element(By.NAME, 'type').send_keys("Test Type")
        self.driver.find_element(By.NAME, 'quantity').send_keys("5")
        Select(self.driver.find_element(By.NAME, 'condition')).select_by_visible_text("Good")
        Select(self.driver.find_element(By.NAME, 'availability')).select_by_visible_text("Available")
        self.driver.find_element(By.NAME, 'location').send_keys("Test Location")
        self.driver.find_element(By.NAME, 'alert_date').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//button[text()="Add Equipment"]').click()
        time.sleep(1)
        
        # Verify equipment is added
        self.assertIn(equipment_name, self.driver.page_source)
        
        # Test updating equipment
        equipment_rows = self.driver.find_elements(By.XPATH, '//table[1]/tbody/tr')
        last_row = equipment_rows[-1]
        update_name = "Updated " + equipment_name
        last_row.find_element(By.NAME, 'name').clear()
        last_row.find_element(By.NAME, 'name').send_keys(update_name)
        last_row.find_element(By.XPATH, './/button[text()="Update"]').click()
        time.sleep(1)
        
        # Verify equipment is updated
        self.assertIn(update_name, self.driver.page_source)

    def test_04_view_equipment_details(self):
        """Test viewing equipment details"""
        self.login("admin", "admin123")
        
        # Verify equipment list is displayed
        equipment_table = self.driver.find_element(By.XPATH, '//table[1]')
        self.assertTrue(equipment_table.is_displayed())
        
        # Verify equipment details are visible
        equipment_rows = self.driver.find_elements(By.XPATH, '//table[1]/tbody/tr')
        self.assertGreater(len(equipment_rows), 0)
        
        # Check details of first equipment item
        first_row = equipment_rows[0]
        details = {
            'id': first_row.find_element(By.XPATH, './td[1]').text,
            'name': first_row.find_element(By.XPATH, './td[2]').text,
            'type': first_row.find_element(By.XPATH, './td[3]').text,
            'quantity': first_row.find_element(By.XPATH, './td[4]').text,
            'condition': first_row.find_element(By.XPATH, './td[5]').text,
            'availability': first_row.find_element(By.XPATH, './td[6]').text,
            'location': first_row.find_element(By.XPATH, './td[7]').text,
            'alert_date': first_row.find_element(By.XPATH, './td[8]').text
        }
        
        self.assertTrue(all(details.values()), "Equipment details should not be empty")

    def test_05_set_alerts(self):
        """Test setting alerts for equipment"""
        self.login("admin", "admin123")
        
        # Set an alert
        equipment_select = Select(self.driver.find_element(By.NAME, 'equipment_id'))
        first_equipment_id = equipment_select.options[0].get_attribute('value')
        equipment_select.select_by_value(first_equipment_id)
        
        alert_select = Select(self.driver.find_element(By.NAME, 'alert_type'))
        alert_select.select_by_visible_text("Maintenance")
        
        self.driver.find_element(By.NAME, 'threshold').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//button[text()="Set Alert"]').click()
        time.sleep(1)
        
        # Verify alert is displayed in alerts table
        alerts_table = self.driver.find_element(By.XPATH, '//table[2]')
        self.assertTrue(alerts_table.is_displayed())
        
        alert_rows = self.driver.find_elements(By.XPATH, '//table[2]/tbody/tr')
        self.assertGreater(len(alert_rows), 0)
        
        # Check if our alert is there
        found = False
        for row in alert_rows:
            if (row.find_element(By.XPATH, './td[1]').text == first_equipment_id and
                row.find_element(By.XPATH, './td[2]').text == "Maintenance"):
                found = True
                break
                
        self.assertTrue(found, "New alert not found in alerts table")

    def test_06_search_equipment(self):
        """Test searching for equipment"""
        self.login("admin", "admin123")
        
        # Search for existing equipment
        search_query = "Microscope"
        self.driver.find_element(By.NAME, 'query').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)
        
        # Verify search results
        equipment_rows = self.driver.find_elements(By.XPATH, '//table[1]/tbody/tr')
        self.assertGreater(len(equipment_rows), 0)
        
        for row in equipment_rows:
            name = row.find_element(By.XPATH, './td[2]').text
            self.assertIn(search_query.lower(), name.lower())

    def test_07_filter_equipment(self):
        """Test filtering equipment"""
        self.login("admin", "admin123")
        
        # Filter by condition
        condition_select = Select(self.driver.find_element(By.NAME, 'condition'))
        condition_select.select_by_visible_text("Good")
        self.driver.find_element(By.XPATH, '//button[text()="Filter"]').click()
        time.sleep(1)
        
        # Verify filtered results
        equipment_rows = self.driver.find_elements(By.XPATH, '//table[1]/tbody/tr')
        self.assertGreater(len(equipment_rows), 0)
        
        for row in equipment_rows:
            condition = row.find_element(By.XPATH, './td[5]').text
            self.assertEqual(condition, "Good")
        
        # Clear filter
        condition_select = Select(self.driver.find_element(By.NAME, 'condition'))
        condition_select.select_by_visible_text("Any")
        self.driver.find_element(By.XPATH, '//button[text()="Filter"]').click()
        time.sleep(1)
        
        # Verify all equipment is displayed again
        all_equipment_rows = self.driver.find_elements(By.XPATH, '//table[1]/tbody/tr')
        self.assertGreater(len(all_equipment_rows), len(equipment_rows))

    def test_08_user_logout(self):
        """Test user logout functionality"""
        self.login("admin", "admin123")
        
        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        
        # Verify redirected to login page
        self.assertIn("Login", self.driver.title)
        
        # Try to access dashboard directly
        self.driver.get('http://localhost:8110/dashboard')
        time.sleep(1)
        
        # Verify redirected back to login page
        self.assertIn("Login", self.driver.title)

    def test_09_data_persistence(self):
        """Test data persistence across sessions"""
        self.login("admin", "admin123")
        
        # Add new equipment
        equipment_name = "Persistent Equipment " + str(int(time.time()))
        self.driver.find_element(By.NAME, 'name').send_keys(equipment_name)
        self.driver.find_element(By.NAME, 'type').send_keys("Persistent Type")
        self.driver.find_element(By.NAME, 'quantity').send_keys("10")
        Select(self.driver.find_element(By.NAME, 'condition')).select_by_visible_text("New")
        Select(self.driver.find_element(By.NAME, 'availability')).select_by_visible_text("Available")
        self.driver.find_element(By.NAME, 'location').send_keys("Persistent Location")
        self.driver.find_element(By.NAME, 'alert_date').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//button[text()="Add Equipment"]').click()
        time.sleep(1)
        
        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        
        # Login again
        self.login("admin", "admin123")
        
        # Verify equipment still exists
        self.assertIn(equipment_name, self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
