import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTripSaverApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8448/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8448/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8448/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Trip Input", self.driver.title)  # Check if redirected to trip input page

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8448/')
        self.login("invalid_user", "invalid_pass")
        self.assertIn("Invalid credentials", self.driver.page_source)  # Check for error message

    def test_input_trip_details(self):
        # Functionality 3: Input Trip Details
        self.login("admin", "admin123")  # Login first
        self.driver.get('http://localhost:8448/trip_input')  # Navigate to trip input page
        self.assertIn("Input Trip Details", self.driver.title)

        # Fill in trip details
        self.driver.find_element(By.NAME, 'start').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-12-25")
        self.driver.find_element(By.XPATH, '//button[text()="Get Suggestions"]').click()

        # Verify suggestions page is displayed
        self.assertIn("Transportation Suggestions", self.driver.title)

        # Attempt to submit with empty fields
        self.driver.get('http://localhost:8448/trip_input')
        self.driver.find_element(By.XPATH, '//button[text()="Get Suggestions"]').click()
        self.assertIn("All fields are required", self.driver.page_source)  # Check for error message

    def test_view_transportation_suggestions(self):
        # Functionality 4: View Transportation Suggestions
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8448/trip_input')
        self.driver.find_element(By.NAME, 'start').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-12-25")
        self.driver.find_element(By.XPATH, '//button[text()="Get Suggestions"]').click()

        # Verify suggestions are displayed
        self.assertIn("Bus", self.driver.page_source)
        self.assertIn("Train", self.driver.page_source)

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)  # Verify redirection to login page

        # Attempt to access trip input page after logout
        self.driver.get('http://localhost:8448/trip_input')
        self.assertIn("Login", self.driver.title)  # Should redirect to login page

if __name__ == '__main__':
    unittest.main()
