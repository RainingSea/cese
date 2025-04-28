import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTripSaverApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8447/')  # Use the port from main.py

    def tearDown(self):
        # Close the web driver session and the subprocess
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8447/register')  # Navigate to registration page
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
        self.driver.get('http://localhost:8447/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing user
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Registration failed", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8447/')  # Navigate to login page
        self.assertIn("Login", self.driver.title)

        # Successful login
        self.login("admin", "admin123")
        self.assertIn("Trip Input", self.driver.title)

        # Unsuccessful login
        self.driver.get('http://localhost:8447/')
        self.login("invalid_user", "invalid_password")
        self.assertIn("Login failed", self.driver.page_source)

    def test_input_trip_details(self):
        # Functionality 3: Input Trip Details
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8447/trip_input')  # Navigate to trip input page
        self.assertIn("Input Trip Details", self.driver.title)

        # Fill in trip details
        self.driver.find_element(By.NAME, 'start').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-12-01")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify that transportation options are displayed
        self.assertIn("Transportation Options", self.driver.title)

        # Attempt to submit with empty fields
        self.driver.get('http://localhost:8447/trip_input')
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        self.assertIn("required", self.driver.page_source)

    def test_view_transportation_suggestions(self):
        # Functionality 4: View Transportation Suggestions
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8447/trip_input')
        self.driver.find_element(By.NAME, 'start').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-12-01")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify transportation options are displayed
        self.assertIn("Transportation Options", self.driver.title)

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")  # Log in first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to access trip input page after logout
        self.driver.get('http://localhost:8447/trip_input')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
