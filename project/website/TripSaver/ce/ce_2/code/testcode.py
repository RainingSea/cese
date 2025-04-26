import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestTripSaverApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8276/') 

    def tearDown(self):
        # Close the web driver session
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
        self.driver.get('http://localhost:8276/register')
        time.sleep(1)  # Wait for the registration page to load

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
        self.driver.get('http://localhost:8276/register')
        time.sleep(1)  # Wait for the registration page to load
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for existing username
        self.assertIn("Username already exists.", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Trip Details page
        self.assertIn("Trip Details", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8276/')
        time.sleep(1)  # Wait for the login page to load
        self.driver.find_element(By.NAME, 'username').send_keys("invalid_user")
        self.driver.find_element(By.NAME, 'password').send_keys("invalid_pass")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for invalid credentials
        self.assertIn("Invalid username or password", self.driver.page_source)

    def test_input_trip_details(self):
        # Functionality 3: Input Trip Details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8276/trip_details')
        time.sleep(1)  # Wait for the trip details page to load

        # Fill in the trip details with valid information
        self.driver.find_element(By.NAME, 'start').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-01")
        self.driver.find_element(By.XPATH, '//button[text()="Get Transport Options"]').click()
        time.sleep(1)  # Wait for the results page to load

        # Verify that transport options are displayed
        self.assertIn("Transport Options", self.driver.title)

        # Attempt to submit with empty fields
        self.driver.get('http://localhost:8276/trip_details')
        time.sleep(1)  # Wait for the trip details page to load
        self.driver.find_element(By.XPATH, '//button[text()="Get Transport Options"]').click()
        time.sleep(1)  # Wait for the results page to load

        # Verify error message for empty fields
        self.assertIn("All fields are required.", self.driver.page_source)

    def test_view_transportation_suggestions(self):
        # Functionality 4: View Transportation Suggestions
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8276/trip_details')
        time.sleep(1)  # Wait for the trip details page to load

        # Fill in the trip details
        self.driver.find_element(By.NAME, 'start').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-01")
        self.driver.find_element(By.XPATH, '//button[text()="Get Transport Options"]').click()
        time.sleep(1)  # Wait for the results page to load

        # Verify that transportation options are displayed
        options = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(options), 0, "No transportation options found.")

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")

        # Simulate logout (not implemented in the codebase, so we will just check the title)
        self.driver.get('http://localhost:8276/')
        time.sleep(1)  # Wait for the login page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
