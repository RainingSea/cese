import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestSportsEquipmentInventoryTracker(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8648/')

    def tearDown(self):
        # Close the web driver session and stop the application
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
        time.sleep(1)

        # Verify the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)  # Assuming it stays on the registration page

    def test_user_login(self):
        # Verify the Login form is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8648/')
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)  # Assuming it stays on the login page

    def test_equipment_management_on_dashboard(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify the equipment management interface is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Input details for a new equipment item and submit
        self.driver.find_element(By.NAME, 'name').send_keys("New Equipment")
        self.driver.find_element(By.NAME, 'type').send_keys("Type")
        self.driver.find_element(By.NAME, 'quantity').send_keys("10")
        self.driver.find_element(By.NAME, 'condition').send_keys("Good")
        self.driver.find_element(By.NAME, 'availability').send_keys("true")
        self.driver.find_element(By.NAME, 'location').send_keys("Location")
        self.driver.find_element(By.NAME, 'add_equipment').click()
        time.sleep(1)

        # Verify the new equipment item is added and displayed
        self.assertIn("New Equipment", self.driver.page_source)

    def test_view_equipment_details(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify a list of available equipment is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Click on a specific equipment item to view its details
        # Assuming clicking is implemented, otherwise this will fail
        self.fail("View equipment details functionality not implemented")

    def test_set_alerts_for_equipment_maintenance(self):
        # Navigate to the Dashboard Page and select an equipment item
        self.login("admin", "admin123")

        # Set a maintenance alert for the equipment
        # Assuming setting alerts is implemented, otherwise this will fail
        self.fail("Set alerts functionality not implemented")

    def test_search_for_equipment(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Enter a specific equipment name in the search bar
        # Assuming search functionality is implemented, otherwise this will fail
        self.fail("Search functionality not implemented")

    def test_filter_equipment_list(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Apply a filter based on equipment condition
        # Assuming filter functionality is implemented, otherwise this will fail
        self.fail("Filter functionality not implemented")

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Logout from the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8648/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_data_persistence(self):
        # Login and add a new equipment item
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'name').send_keys("Persistent Equipment")
        self.driver.find_element(By.NAME, 'type').send_keys("Type")
        self.driver.find_element(By.NAME, 'quantity').send_keys("5")
        self.driver.find_element(By.NAME, 'condition').send_keys("New")
        self.driver.find_element(By.NAME, 'availability').send_keys("true")
        self.driver.find_element(By.NAME, 'location').send_keys("Location")
        self.driver.find_element(By.NAME, 'add_equipment').click()
        time.sleep(1)

        # Logout and close the application
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.driver.quit()
        self.process.terminate()

        # Reopen the application and log in again
        self.setUp()
        self.login("admin", "admin123")

        # Verify the previously added equipment item is still present
        self.assertIn("Persistent Equipment", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
