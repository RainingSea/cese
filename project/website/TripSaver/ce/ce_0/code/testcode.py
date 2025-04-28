import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTripSaverApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8446/')  # Accessing the login page

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
        self.driver.get('http://localhost:8446/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify successful registration
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8446/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already exists!", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Trip Input", self.driver.title)  # Check if redirected to Trip Input page

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8446/')
        self.login("admin", "wrong_password")
        self.assertIn("Login", self.driver.title)  # Should still be on login page

    def test_input_trip_details(self):
        # Functionality 3: Input Trip Details
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8446/trip_input')  # Navigate to trip input page
        self.assertIn("Input Trip Details", self.driver.title)

        # Fill in trip details
        self.driver.find_element(By.NAME, 'start').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-15")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify that transportation options are displayed
        self.assertIn("Transportation Options", self.driver.title)

        # Attempt to submit with empty fields
        self.driver.get('http://localhost:8446/trip_input')
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        self.assertIn("This field is required.", self.driver.page_source)

    def test_view_transportation_suggestions(self):
        # Functionality 4: View Transportation Suggestions
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8446/trip_input')
        self.driver.find_element(By.NAME, 'start').send_keys("Chicago")
        self.driver.find_element(By.NAME, 'destination').send_keys("Miami")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-20")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify transportation options are displayed
        options = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(options), 0, "No transportation options found.")

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8446/')  # Navigate to login page
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)  # Verify redirection to login page

if __name__ == '__main__':
    unittest.main()
