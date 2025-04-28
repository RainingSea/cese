import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestVehicleMaintenanceTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8451/')  # Access the login page

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
        self.driver.get('http://localhost:8451/register')  # Navigate to registration page
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
        self.driver.get('http://localhost:8451/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing user
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Check for error message (assuming an error message is displayed)
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Vehicle Information", self.driver.title)  # Check for successful login

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8451/')
        self.login("invalid_user", "wrong_password")
        self.assertIn("Invalid credentials", self.driver.page_source)  # Check for error message

    def test_input_vehicle_information(self):
        # Functionality 3: Input Vehicle Information
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8451/vehicle_info')  # Navigate to vehicle info page
        self.assertIn("Vehicle Information", self.driver.title)

        # Add a vehicle
        self.driver.find_element(By.NAME, 'make').send_keys("Ford")
        self.driver.find_element(By.NAME, 'model').send_keys("Focus")
        self.driver.find_element(By.NAME, 'year').send_keys("2021")
        self.driver.find_element(By.NAME, 'mileage').send_keys("10000")
        self.driver.find_element(By.XPATH, '//button[text()="Add Vehicle"]').click()

        # Verify vehicle addition (assuming a success message is displayed)
        self.assertIn("Vehicle added successfully", self.driver.page_source)

        # Attempt to add a vehicle with invalid mileage
        self.driver.find_element(By.NAME, 'mileage').clear()
        self.driver.find_element(By.NAME, 'mileage').send_keys("-500")  # Invalid mileage
        self.driver.find_element(By.XPATH, '//button[text()="Add Vehicle"]').click()

        # Check for error message
        self.assertIn("Invalid mileage", self.driver.page_source)

    def test_track_regular_maintenance_tasks(self):
        # Functionality 4: Track Regular Maintenance Tasks
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8451/maintenance')  # Navigate to maintenance page
        self.assertIn("Maintenance Tracking", self.driver.title)

        # Add a maintenance task
        self.driver.find_element(By.NAME, 'vehicle_id').send_keys("0")  # Assuming vehicle ID 0 exists
        self.driver.find_element(By.NAME, 'task').send_keys("Oil Change")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-03-01")
        self.driver.find_element(By.NAME, 'mileage').send_keys("15000")
        self.driver.find_element(By.XPATH, '//button[text()="Add Maintenance"]').click()

        # Verify maintenance task addition
        self.assertIn("Maintenance task added successfully", self.driver.page_source)

        # Attempt to add a maintenance task without specifying a task type
        self.driver.find_element(By.NAME, 'task').clear()  # Clear task field
        self.driver.find_element(By.XPATH, '//button[text()="Add Maintenance"]').click()

        # Check for error message
        self.assertIn("Task type is required", self.driver.page_source)

    def test_view_maintenance_history(self):
        # Functionality 6: View Maintenance History
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8451/maintenance')  # Navigate to maintenance page

        # Check for existing maintenance records
        self.assertIn("Oil Change", self.driver.page_source)  # Check for a known record

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")  # Log in first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click logout
        self.assertIn("Login", self.driver.title)  # Verify redirection to login page

if __name__ == '__main__':
    unittest.main()
