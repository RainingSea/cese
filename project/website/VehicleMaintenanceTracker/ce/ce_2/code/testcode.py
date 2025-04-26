import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestVehicleMaintenanceTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8280/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
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
        self.driver.get('http://localhost:8280/register')  # Navigate to registration page
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
        self.driver.get('http://localhost:8280/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message
        self.assertIn("Registration failed", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Vehicle Information", self.driver.title)  # Check if redirected to the dashboard

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8280/')
        self.login("invalid_user", "invalid_password")
        time.sleep(1)  # Wait for the next page to load

        # Verify error message
        self.assertIn("Login", self.driver.title)  # Should still be on login page

    def test_input_vehicle_information(self):
        # Functionality 3: Input Vehicle Information
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8280/vehicle_info')  # Navigate to vehicle info page
        self.assertIn("Vehicle Information", self.driver.title)

        # Add a vehicle
        self.driver.find_element(By.NAME, 'make').send_keys("Ford")
        self.driver.find_element(By.NAME, 'model').send_keys("Focus")
        self.driver.find_element(By.NAME, 'year').send_keys("2021")
        self.driver.find_element(By.NAME, 'mileage').send_keys("10000")
        self.driver.find_element(By.XPATH, '//button[text()="Add Vehicle"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify vehicle was added
        self.assertIn("Ford Focus", self.driver.page_source)

        # Attempt to add invalid vehicle information (negative mileage)
        self.driver.find_element(By.NAME, 'make').send_keys("Chevrolet")
        self.driver.find_element(By.NAME, 'model').send_keys("Malibu")
        self.driver.find_element(By.NAME, 'year').send_keys("2022")
        self.driver.find_element(By.NAME, 'mileage').send_keys("-5000")  # Invalid mileage
        self.driver.find_element(By.XPATH, '//button[text()="Add Vehicle"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message
        self.assertIn("Invalid input", self.driver.page_source)

    def test_track_maintenance_tasks(self):
        # Functionality 4: Track Regular Maintenance Tasks
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8280/maintenance')  # Navigate to maintenance page
        self.assertIn("Maintenance Tracking", self.driver.title)

        # Add a maintenance task
        self.driver.find_element(By.NAME, 'vehicle_id').send_keys("1")
        self.driver.find_element(By.NAME, 'task').send_keys("Oil Change")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-01")
        self.driver.find_element(By.XPATH, '//button[text()="Add Maintenance"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify maintenance task was added
        self.assertIn("Oil Change", self.driver.page_source)

        # Attempt to add a maintenance task without specifying a task type
        self.driver.find_element(By.NAME, 'vehicle_id').send_keys("1")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-15")  # No task
        self.driver.find_element(By.XPATH, '//button[text()="Add Maintenance"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message
        self.assertIn("Task is required", self.driver.page_source)

    def test_view_maintenance_history(self):
        # Functionality 6: View Maintenance History
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8280/maintenance')  # Navigate to maintenance page
        self.assertIn("Maintenance Tracking", self.driver.title)

        # Check if maintenance history is displayed
        self.assertIn("Oil Change", self.driver.page_source)
        self.assertIn("Tire Rotation", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")  # Log in first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
