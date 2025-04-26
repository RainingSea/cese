import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestVehicleMaintenanceTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8278/')  # Use the assigned port from main.py

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8278/register')  # Navigate to Registration Page
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
        self.driver.get('http://localhost:8278/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message
        self.assertIn("Registration failed", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8278/')  # Navigate to Login Page
        self.assertIn("Login", self.driver.title)

        # Successful login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Unsuccessful login
        self.driver.get('http://localhost:8278/')
        self.login("admin", "wrong_password")
        self.assertIn("Login", self.driver.title)  # Should still be on login page

    def test_input_vehicle_information(self):
        # Functionality 3: Input Vehicle Information
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8278/dashboard')  # Navigate to Vehicle Information Page
        self.assertIn("Vehicle Dashboard", self.driver.title)

        # Add vehicle
        self.driver.find_element(By.NAME, 'make').send_keys("Ford")
        self.driver.find_element(By.NAME, 'model').send_keys("Mustang")
        self.driver.find_element(By.NAME, 'year').send_keys("2021")
        self.driver.find_element(By.NAME, 'mileage').send_keys("5000")
        self.driver.find_element(By.XPATH, '//button[text()="Add Vehicle"]').click()

        # Verify vehicle is added
        self.assertIn("Ford Mustang", self.driver.page_source)

        # Attempt to add invalid vehicle (negative mileage)
        self.driver.find_element(By.NAME, 'make').send_keys("Chevrolet")
        self.driver.find_element(By.NAME, 'model').send_keys("Camaro")
        self.driver.find_element(By.NAME, 'year').send_keys("2021")
        self.driver.find_element(By.NAME, 'mileage').send_keys("-1000")
        self.driver.find_element(By.XPATH, '//button[text()="Add Vehicle"]').click()

        # Verify error message
        self.assertIn("Invalid input", self.driver.page_source)

    def test_view_maintenance_history(self):
        # Functionality 6: View Maintenance History
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8278/maintenance')  # Navigate to Maintenance History Page
        self.assertIn("Maintenance History", self.driver.title)

        # Check if maintenance records are displayed
        self.assertIn("Oil Change", self.driver.page_source)
        self.assertIn("Tire Rotation", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8278/')  # Navigate to Dashboard Page

        # Click logout button (assuming there's a logout button)
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
