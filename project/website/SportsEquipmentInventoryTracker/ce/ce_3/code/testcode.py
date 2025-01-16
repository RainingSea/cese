import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestSportsEquipmentInventoryTracker(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8650/')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.get('http://localhost:8650/register')
        self.assertIn("Registration", self.driver.title)

        # Register with a new username
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8650/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Check for error message (not implemented in UI, so this will fail)
        self.fail("Error message for existing username not implemented")

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8650/')
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8650/')
        self.login("invalid_user", "invalid_pass")
        self.assertIn("Login", self.driver.title)

    def test_equipment_management(self):
        # Login and navigate to Dashboard
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Add new equipment
        self.driver.find_element(By.NAME, 'name').send_keys("Bulldozer")
        self.driver.find_element(By.NAME, 'type').send_keys("Heavy")
        self.driver.find_element(By.NAME, 'quantity').send_keys("3")
        self.driver.find_element(By.NAME, 'condition').send_keys("New")
        self.driver.find_element(By.NAME, 'availability').click()
        self.driver.find_element(By.NAME, 'location').send_keys("Site C")
        self.driver.find_element(By.NAME, 'maintenance_alert').send_keys("Check every month")
        self.driver.find_element(By.XPATH, '//button[text()="Add Equipment"]').click()
        time.sleep(1)

        # Verify new equipment is added
        self.assertIn("Bulldozer", self.driver.page_source)

        # Update equipment (not implemented, so this will fail)
        self.fail("Update equipment functionality not implemented")

    def test_view_equipment_details(self):
        # Login and navigate to Dashboard
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Verify equipment details are displayed
        self.assertIn("Excavator", self.driver.page_source)

    def test_set_maintenance_alerts(self):
        # Login and navigate to Dashboard
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Set maintenance alert (not implemented, so this will fail)
        self.fail("Set maintenance alert functionality not implemented")

    def test_search_for_equipment(self):
        # Login and navigate to Dashboard
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Search for equipment (not implemented, so this will fail)
        self.fail("Search for equipment functionality not implemented")

    def test_filter_equipment_list(self):
        # Login and navigate to Dashboard
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Filter equipment list (not implemented, so this will fail)
        self.fail("Filter equipment list functionality not implemented")

    def test_user_logout(self):
        # Login and navigate to Dashboard
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

    def test_data_persistence(self):
        # Login and add new equipment
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Add new equipment
        self.driver.find_element(By.NAME, 'name').send_keys("Crane")
        self.driver.find_element(By.NAME, 'type').send_keys("Heavy")
        self.driver.find_element(By.NAME, 'quantity').send_keys("2")
        self.driver.find_element(By.NAME, 'condition').send_keys("Good")
        self.driver.find_element(By.NAME, 'availability').click()
        self.driver.find_element(By.NAME, 'location').send_keys("Site D")
        self.driver.find_element(By.NAME, 'maintenance_alert').send_keys("Check every two months")
        self.driver.find_element(By.XPATH, '//button[text()="Add Equipment"]').click()
        time.sleep(1)

        # Logout and close the application
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.driver.quit()
        self.process.terminate()

        # Reopen the application and verify data persistence
        self.setUp()
        self.login("admin", "admin123")
        self.assertIn("Crane", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
