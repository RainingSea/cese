import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestVehicleMaintenanceTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8279/')  # Access the login page

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
        self.driver.get('http://localhost:8279/register')  # Navigate to Registration Page
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
        self.driver.get('http://localhost:8279/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing user
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("User already exists.", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Vehicle Input", self.driver.title)  # Check redirection to Vehicle Input Page

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8279/')
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Login", self.driver.title)  # Check if still on login page

    def test_input_vehicle_information(self):
        # Functionality 3: Input Vehicle Information
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8279/vehicle')  # Navigate to Vehicle Input Page
        self.assertIn("Add Vehicle", self.driver.title)

        # Add valid vehicle information
        self.driver.find_element(By.NAME, 'make').send_keys("Ford")
        self.driver.find_element(By.NAME, 'model').send_keys("Focus")
        self.driver.find_element(By.NAME, 'year').send_keys("2021")
        self.driver.find_element(By.NAME, 'mileage').send_keys("5000")
        self.driver.find_element(By.XPATH, '//button[text()="Add Vehicle"]').click()

        # Verify vehicle information is saved (redirected back to input page)
        self.assertIn("Add Vehicle", self.driver.title)

    def test_track_maintenance_tasks(self):
        # Functionality 4: Track Regular Maintenance Tasks
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8279/maintenance')  # Navigate to Maintenance Tracker Page
        self.assertIn("Maintenance Tracking", self.driver.title)

        # Add a valid maintenance task
        self.driver.find_element(By.NAME, 'vehicle_id').send_keys("1")
        self.driver.find_element(By.NAME, 'task').send_keys("Oil Change")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-03-01")
        self.driver.find_element(By.XPATH, '//button[text()="Add Maintenance Record"]').click()

        # Verify maintenance task is saved (redirected back to maintenance page)
        self.assertIn("Maintenance Tracking", self.driver.title)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8279/')  # Navigate to Dashboard
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click logout
        self.assertIn("Login", self.driver.title)  # Verify redirection to login page

if __name__ == '__main__':
    unittest.main()
