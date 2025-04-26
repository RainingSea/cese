import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestSportsEquipmentInventoryTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8252/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8252/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8252/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Check for error message (not implemented in the codebase)
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8252/')
        self.login("invalid_user", "invalid_password")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_equipment_management(self):
        # Functionality 3: Equipment Management on Dashboard Page
        self.login("admin", "admin123")  # Log in to access the dashboard
        self.assertIn("Dashboard", self.driver.title)

        # Add new equipment
        self.driver.find_element(By.NAME, 'name').send_keys("New Tennis Racket")
        self.driver.find_element(By.NAME, 'type').send_keys("Sports")
        self.driver.find_element(By.NAME, 'quantity').send_keys("5")
        self.driver.find_element(By.NAME, 'condition').send_keys("Good")
        self.driver.find_element(By.NAME, 'location').send_keys("Storage Room A")
        self.driver.find_element(By.XPATH, '//button[text()="Add Equipment"]').click()

        # Verify that the new equipment is displayed
        self.assertIn("New Tennis Racket", self.driver.page_source)

        # Update existing equipment (not implemented in the codebase)
        self.fail("Update equipment functionality not implemented")

    def test_view_equipment_details(self):
        # Functionality 4: View Equipment Details
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Click on a specific equipment item (not implemented in the codebase)
        self.fail("View equipment details functionality not implemented")

    def test_set_alerts(self):
        # Functionality 5: Set Alerts for Equipment Maintenance
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Set a maintenance alert for an equipment item (not implemented in the codebase)
        self.fail("Set alerts functionality not implemented")

    def test_search_equipment(self):
        # Functionality 6: Search for Equipment
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Search for equipment (not implemented in the codebase)
        self.fail("Search equipment functionality not implemented")

    def test_filter_equipment(self):
        # Functionality 7: Filter Equipment List
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Apply a filter based on equipment condition (not implemented in the codebase)
        self.fail("Filter equipment functionality not implemented")

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_data_persistence(self):
        # Functionality 9: Data Persistence
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'name').send_keys("Persistent Equipment")
        self.driver.find_element(By.NAME, 'type').send_keys("Sports")
        self.driver.find_element(By.NAME, 'quantity').send_keys("10")
        self.driver.find_element(By.NAME, 'condition').send_keys("New")
        self.driver.find_element(By.NAME, 'location').send_keys("Storage Room B")
        self.driver.find_element(By.XPATH, '//button[text()="Add Equipment"]').click()

        # Logout and log back in
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.login("admin", "admin123")

        # Verify that the previously added equipment is still present (not implemented in the codebase)
        self.fail("Data persistence functionality not implemented")

if __name__ == '__main__':
    unittest.main()
