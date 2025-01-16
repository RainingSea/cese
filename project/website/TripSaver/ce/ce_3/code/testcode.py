import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTripSaverApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8680/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.get('http://localhost:8680/register')
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8680/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Expectation: Error message for existing username (not implemented in codebase)
        self.fail("Error message for existing username not implemented")

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Trip Input", self.driver.title)

        # Invalid login
        self.driver.get('http://localhost:8680/')
        self.login("invalid_user", "invalid_pass")
        self.assertIn("Login", self.driver.title)

    def test_input_trip_details(self):
        # Login and navigate to Trip Details input page
        self.login("admin", "admin123")
        self.assertIn("Trip Input", self.driver.title)

        # Fill in trip details and submit
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-10-10")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Verify redirection to suggestions page
        self.assertIn("Suggestions", self.driver.title)

        # Attempt to submit with empty fields
        self.driver.get('http://localhost:8680/trip_input')
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Expectation: Error message for empty fields (not implemented in codebase)
        self.fail("Error message for empty fields not implemented")

    def test_view_transportation_suggestions(self):
        # Login and input trip details
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-10-10")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Verify transportation suggestions are displayed
        suggestions = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(suggestions), 0, "No transportation suggestions found.")

    def test_save_preferred_transportation_options(self):
        # Expectation: Save preferred option (not implemented in codebase)
        self.fail("Save preferred transportation option not implemented")

    def test_user_logout(self):
        # Expectation: User logout (not implemented in codebase)
        self.fail("User logout functionality not implemented")

    def test_view_estimated_costs_and_travel_times(self):
        # Expectation: View estimated costs and travel times (not implemented in codebase)
        self.fail("View estimated costs and travel times not implemented")

    def test_compare_transportation_options(self):
        # Expectation: Compare transportation options (not implemented in codebase)
        self.fail("Compare transportation options not implemented")

if __name__ == '__main__':
    unittest.main()
