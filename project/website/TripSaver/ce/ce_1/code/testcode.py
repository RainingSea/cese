import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTripSaverApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8678/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify successful registration
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already exists!", self.driver.page_source)

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Login with valid credentials
        self.login("admin", "admin123")

        # Verify redirection to the Trip Input Page
        self.assertIn("Trip Input", self.driver.title)

        # Login with invalid credentials
        self.driver.get('http://localhost:8678/')  # Navigate back to login page
        self.login("invalid_user", "invalid_pass")

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials!", self.driver.page_source)

    def test_input_trip_details(self):
        # Login and navigate to the Trip Input Page
        self.login("admin", "admin123")

        # Verify the Trip Input form is displayed
        self.assertIn("Trip Input", self.driver.title)

        # Fill in trip details and submit
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-01")
        self.driver.find_element(By.XPATH, '//button[text()="Find Options"]').click()

        # Verify redirection to the Results Page
        self.assertIn("Transportation Options", self.driver.title)

        # Leave fields empty and attempt to submit
        self.driver.get('http://localhost:8678/trip_input')  # Navigate back to trip input page
        self.driver.find_element(By.XPATH, '//button[text()="Find Options"]').click()

        # Verify error message for empty fields
        self.assertIn("This field is required", self.driver.page_source)

    def test_view_transportation_suggestions(self):
        # Login and input trip details
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-01")
        self.driver.find_element(By.XPATH, '//button[text()="Find Options"]').click()

        # Verify transportation options are displayed
        self.assertIn("Bus", self.driver.page_source)
        self.assertIn("Train", self.driver.page_source)
        self.assertIn("Flight", self.driver.page_source)

    def test_save_preferred_transportation_options(self):
        # This functionality is not implemented in the codebase
        self.fail("Save Preferred Transportation Options functionality not implemented")

    def test_user_logout(self):
        # Login and logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Trip Input Page after logout
        self.driver.get('http://localhost:8678/trip_input')

        # Verify redirection back to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_view_estimated_costs_and_travel_times(self):
        # This functionality is not implemented in the codebase
        self.fail("View Estimated Costs and Travel Times functionality not implemented")

    def test_compare_transportation_options(self):
        # This functionality is not implemented in the codebase
        self.fail("Compare Transportation Options functionality not implemented")

if __name__ == '__main__':
    unittest.main()
