import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestSportsEquipmentInventoryTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8423/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8423/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8423/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8423/')
        self.login("invalid_user", "invalid_password")
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_dashboard_equipment_management(self):
        # Functionality 3: Equipment Management on Dashboard Page
        self.login("admin", "admin123")  # Login successfully
        self.assertIn("Dashboard", self.driver.title)

        # Add new equipment
        self.driver.find_element(By.XPATH, '//button[text()="Add Equipment"]').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'name').send_keys("New Drill")
        self.driver.find_element(By.NAME, 'type').send_keys("Power Tool")
        self.driver.find_element(By.NAME, 'quantity').send_keys("5")
        self.driver.find_element(By.NAME, 'condition').send_keys("New")
        self.driver.find_element(By.NAME, 'location').send_keys("Warehouse A")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the new equipment is displayed
        self.assertIn("New Drill", self.driver.page_source)

        # Update existing equipment
        self.driver.find_element(By.XPATH, '//button[text()="Edit New Drill"]').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'quantity').clear()
        self.driver.find_element(By.NAME, 'quantity').send_keys("10")
        self.driver.find_element(By.XPATH, '//button[text()="Update"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the updated information is reflected
        self.assertIn("10", self.driver.page_source)

    def test_view_equipment_details(self):
        # Functionality 4: View Equipment Details
        self.login("admin", "admin123")  # Login successfully
        self.assertIn("Dashboard", self.driver.title)

        # Click on a specific equipment item
        self.driver.find_element(By.XPATH, '//button[text()="View New Drill"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify detailed information is displayed
        self.assertIn("New Drill", self.driver.page_source)

    def test_search_equipment(self):
        # Functionality 6: Search for Equipment
        self.login("admin", "admin123")  # Login successfully
        self.assertIn("Dashboard", self.driver.title)

        # Search for equipment by name
        self.driver.find_element(By.NAME, 'search').send_keys("New Drill")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the equipment list is filtered
        self.assertIn("New Drill", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")  # Login successfully
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
