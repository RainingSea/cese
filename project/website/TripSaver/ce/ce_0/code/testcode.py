import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTripSaverApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8274/')  # Access the login page

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
        self.driver.get('http://localhost:8274/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8274/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Check for error message
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8274/')
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_input_trip_details(self):
        # Functionality 3: Input Trip Details
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8274/trip_input')  # Navigate to trip input page
        self.assertIn("Input Trip Details", self.driver.title)

        # Fill in trip details
        self.driver.find_element(By.NAME, 'start').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-01")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify redirection to suggestions page
        self.assertIn("Transportation Suggestions", self.driver.title)

        # Attempt to submit with empty fields
        self.driver.get('http://localhost:8274/trip_input')
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()  # Submit without filling
        self.assertIn("All fields are required", self.driver.page_source)

    def test_view_transportation_suggestions(self):
        # Functionality 4: View Transportation Suggestions
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8274/trip_input')
        self.driver.find_element(By.NAME, 'start').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-01")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify suggestions are displayed
        self.assertIn("Bus", self.driver.page_source)
        self.assertIn("Train", self.driver.page_source)

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")  # Log in first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the dashboard after logging out
        self.driver.get('http://localhost:8274/')
        self.login("admin", "admin123")  # Log in again
        self.assertIn("Dashboard", self.driver.title)

if __name__ == '__main__':
    unittest.main()
