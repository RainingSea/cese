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
        self.driver.get('http://localhost:8647/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and terminate the application
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
        self.driver.find_element(By.LINK_TEXT, "Register here").click()
        time.sleep(1)

        # Verify the registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify registration success
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.find_element(By.LINK_TEXT, "Register here").click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("Username already exists!", self.driver.page_source)

    def test_user_login(self):
        # Verify the login form is displayed
        self.assertIn("Login", self.driver.title)

        # Perform login with valid credentials
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Perform login with invalid credentials
        self.driver.get('http://localhost:8647/')  # Navigate back to login page
        self.login("invalid_user", "invalid_pass")
        self.assertIn("Invalid username or password!", self.driver.page_source)

    def test_equipment_management(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify the equipment management interface is displayed
        self.assertIn("Equipment Dashboard", self.driver.page_source)

        # Add a new equipment item
        self.driver.find_element(By.NAME, 'name').send_keys("Volleyball")
        self.driver.find_element(By.NAME, 'quantity').send_keys("12")
        self.driver.find_element(By.NAME, 'condition').send_keys("New")
        self.driver.find_element(By.NAME, 'location').send_keys("Court 2")
        self.driver.find_element(By.XPATH, '//button[text()="Add Equipment"]').click()
        time.sleep(1)

        # Verify the new equipment item is added
        self.assertIn("Volleyball", self.driver.page_source)

        # Update an existing equipment item
        # Note: Update functionality is not implemented in the codebase, so this test will fail
        self.fail("Update functionality not implemented")

    def test_view_equipment_details(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify the list of available equipment is displayed
        equipment_list = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(equipment_list), 0, "No equipment items found.")

        # Click on a specific equipment item to view its details
        # Note: Viewing detailed information is not implemented in the codebase, so this test will fail
        self.fail("View equipment details functionality not implemented")

    def test_set_alerts_for_equipment_maintenance(self):
        # Note: This functionality is not implemented in the codebase, so this test will fail
        self.fail("Set alerts for equipment maintenance functionality not implemented")

    def test_search_for_equipment(self):
        # Note: This functionality is not implemented in the codebase, so this test will fail
        self.fail("Search for equipment functionality not implemented")

    def test_filter_equipment_list(self):
        # Note: This functionality is not implemented in the codebase, so this test will fail
        self.fail("Filter equipment list functionality not implemented")

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Perform logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8647/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_data_persistence(self):
        # Note: This functionality is not implemented in the codebase, so this test will fail
        self.fail("Data persistence functionality not implemented")

if __name__ == '__main__':
    unittest.main()
