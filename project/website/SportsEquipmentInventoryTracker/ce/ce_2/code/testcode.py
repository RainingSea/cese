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
        self.driver.get('http://localhost:8649/') 

    def tearDown(self):
        # Close the web driver session and terminate the application process
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
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)  # Assuming it stays on the same page

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8649/')  # Navigate back to login
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)  # Assuming it stays on the same page

    def test_equipment_management_on_dashboard(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Input details for a new equipment item and submit
        self.driver.find_element(By.NAME, 'name').send_keys("Chair")
        self.driver.find_element(By.NAME, 'type').send_keys("Furniture")
        self.driver.find_element(By.NAME, 'quantity').send_keys("15")
        self.driver.find_element(By.NAME, 'condition').send_keys("New")
        self.driver.find_element(By.NAME, 'location').send_keys("Room 104")
        self.driver.find_element(By.XPATH, '//button[text()="Add Equipment"]').click()
        time.sleep(1)  # Wait for the equipment to be added

        # Verify the new equipment item is added to the inventory
        self.assertIn("Chair", self.driver.page_source)

    def test_view_equipment_details(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Verify a list of available equipment is displayed
        equipment_list = self.driver.find_elements(By.TAG_NAME, 'tr')
        self.assertGreater(len(equipment_list), 1, "No equipment items found.")

    def test_set_alerts_for_equipment_maintenance(self):
        # Functionality not implemented
        self.fail("Set Alerts for Equipment Maintenance not implemented")

    def test_search_for_equipment(self):
        # Functionality not implemented
        self.fail("Search for Equipment not implemented")

    def test_filter_equipment_list(self):
        # Functionality not implemented
        self.fail("Filter Equipment List not implemented")

    def test_user_logout(self):
        # Login successfully
        self.login("admin", "admin123")

        # Logout from the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8649/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_data_persistence(self):
        # Functionality not implemented
        self.fail("Data Persistence not implemented")

if __name__ == '__main__':
    unittest.main()
