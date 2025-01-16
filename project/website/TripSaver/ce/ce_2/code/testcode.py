import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTripSaverApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        # Initialize the webdriver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8679/') 

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
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("username is already taken", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Dashboard Page
        self.assertNotIn("Login", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8679/')
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("credentials are incorrect", self.driver.page_source)

    def test_input_trip_details(self):
        # Login successfully
        self.login("admin", "admin123")

        # Navigate to the Trip Details input page
        self.driver.find_element(By.LINK_TEXT, 'Input Trip').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the Trip Details input form is displayed
        self.assertIn("Input Trip", self.driver.title)

        # Fill in the trip details with valid information and submit
        self.driver.find_element(By.NAME, 'starting_point').send_keys("Boston")
        self.driver.find_element(By.NAME, 'destination').send_keys("Miami")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-10")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Trip"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the suggestions page
        self.assertIn("Results", self.driver.title)

        # Leave one or more fields empty and attempt to submit
        self.driver.get('http://localhost:8679/trip_input')
        self.driver.find_element(By.NAME, 'starting_point').send_keys("")
        self.driver.find_element(By.NAME, 'destination').send_keys("Miami")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-10")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Trip"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("all fields are required", self.driver.page_source)

    def test_view_transportation_suggestions(self):
        # Login and input trip details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8679/trip_input')
        self.driver.find_element(By.NAME, 'starting_point').send_keys("Boston")
        self.driver.find_element(By.NAME, 'destination').send_keys("Miami")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-10")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Trip"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify transportation suggestions are displayed
        self.assertIn("Transportation Options", self.driver.page_source)

    def test_save_preferred_transportation_options(self):
        # Functionality not implemented
        self.fail("Functionality not implemented")

    def test_user_logout(self):
        # Functionality not implemented
        self.fail("Functionality not implemented")

    def test_view_estimated_costs_and_travel_times(self):
        # Functionality not implemented
        self.fail("Functionality not implemented")

    def test_compare_transportation_options(self):
        # Functionality not implemented
        self.fail("Functionality not implemented")

if __name__ == '__main__':
    unittest.main()
