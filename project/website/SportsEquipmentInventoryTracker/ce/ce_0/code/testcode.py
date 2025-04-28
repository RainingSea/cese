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
        self.driver.get('http://localhost:8422/')  # Access the login page

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
        self.driver.get('http://localhost:8422/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8422/register')  # Navigate to registration page
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
        self.driver.get('http://localhost:8422/')  # Navigate to login page
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Login", self.driver.title)  # Should remain on login page

    def test_equipment_management(self):
        # Functionality 3: Equipment Management on Dashboard Page
        self.login("admin", "admin123")  # Login successfully
        self.assertIn("Dashboard", self.driver.title)

        # Add new equipment
        self.driver.find_element(By.NAME, 'name').send_keys("New Projector")
        self.driver.find_element(By.NAME, 'type').send_keys("Electronics")
        self.driver.find_element(By.NAME, 'quantity').send_keys("5")
        self.driver.find_element(By.NAME, 'condition').send_keys("Good")
        self.driver.find_element(By.NAME, 'location').send_keys("Room A")
        self.driver.find_element(By.XPATH, '//button[text()="Add Equipment"]').click()
        time.sleep(1)  # Wait for the equipment to be added

        # Verify the new equipment is displayed
        self.assertIn("New Projector", self.driver.page_source)

        # Update existing equipment
        self.driver.find_element(By.NAME, 'name').clear()
        self.driver.find_element(By.NAME, 'name').send_keys("Projector")  # Existing equipment
        self.driver.find_element(By.NAME, 'quantity').clear()
        self.driver.find_element(By.NAME, 'quantity').send_keys("10")
        self.driver.find_element(By.XPATH, '//button[text()="Update Equipment"]').click()
        time.sleep(1)  # Wait for the equipment to be updated

        # Verify the updated equipment is displayed
        self.assertIn("10", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")  # Login successfully
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_data_persistence(self):
        # Functionality 9: Data Persistence
        self.login("admin", "admin123")  # Login successfully
        self.driver.find_element(By.NAME, 'name').send_keys("Persistent Equipment")
        self.driver.find_element(By.NAME, 'type').send_keys("Electronics")
        self.driver.find_element(By.NAME, 'quantity').send_keys("3")
        self.driver.find_element(By.NAME, 'condition').send_keys("New")
        self.driver.find_element(By.NAME, 'location').send_keys("Room B")
        self.driver.find_element(By.XPATH, '//button[text()="Add Equipment"]').click()
        time.sleep(1)  # Wait for the equipment to be added

        # Logout and close the application
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Reopen the application and log in again
        self.driver.get('http://localhost:8422/')
        self.login("admin", "admin123")  # Login successfully

        # Verify that the previously added equipment is still present
        self.assertIn("Persistent Equipment", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
