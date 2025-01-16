import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTripSaverApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8681/')

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

        # Enter a valid username and password
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify registration success
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Registration failed", self.driver.page_source)

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify redirection to the Dashboard Page
        self.assertIn("Trip Input", self.driver.page_source)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8681/')
        self.login("invalid_user", "invalid_pass")

        # Verify error message for incorrect credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_input_trip_details(self):
        # Login and navigate to the Trip Details input page
        self.login("admin", "admin123")

        # Verify the Trip Details input form is displayed
        self.assertIn("Input Trip Details", self.driver.page_source)

        # Fill in the trip details and submit
        self.driver.find_element(By.NAME, 'starting_point').send_keys('New York')
        self.driver.find_element(By.NAME, 'destination').send_keys('Boston')
        self.driver.find_element(By.NAME, 'travel_date').send_keys('2023-12-25')
        self.driver.find_element(By.XPATH, '//button[text()="Save Trip"]').click()

        # Verify trip details are saved successfully
        self.assertIn("Trip saved successfully", self.driver.page_source)

        # Leave one or more fields empty and attempt to submit
        self.driver.get('http://localhost:8681/trip_input')
        self.driver.find_element(By.NAME, 'starting_point').send_keys('')
        self.driver.find_element(By.NAME, 'destination').send_keys('Boston')
        self.driver.find_element(By.NAME, 'travel_date').send_keys('2023-12-25')
        self.driver.find_element(By.XPATH, '//button[text()="Save Trip"]').click()

        # Verify error message for empty fields
        self.assertIn("This field is required", self.driver.page_source)

    def test_view_transportation_suggestions(self):
        # Functionality not implemented
        self.fail("Functionality not implemented")

    def test_save_preferred_transportation_options(self):
        # Functionality not implemented
        self.fail("Functionality not implemented")

    def test_user_logout(self):
        # Login and then logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8681/trip_input')
        self.assertIn("Login", self.driver.title)

    def test_view_estimated_costs_and_travel_times(self):
        # Functionality not implemented
        self.fail("Functionality not implemented")

    def test_compare_transportation_options(self):
        # Functionality not implemented
        self.fail("Functionality not implemented")

if __name__ == '__main__':
    unittest.main()
