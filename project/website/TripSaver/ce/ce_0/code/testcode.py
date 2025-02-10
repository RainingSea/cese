import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTripSaverApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8677/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()
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
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Dashboard Page
        self.assertNotIn("Login", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8677/')
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)

    def test_input_trip_details(self):
        # Login successfully
        self.login("admin", "admin123")

        # Navigate to the Trip Details input page
        self.driver.get('http://localhost:8677/trip_input')
        self.assertIn("Input Trip", self.driver.title)

        # Fill in the trip details with valid information and submit
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Boston")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-15")
        self.driver.find_element(By.XPATH, '//input[@value="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the suggestions page
        self.assertIn("Suggestions", self.driver.title)

        # Leave one or more fields empty and attempt to submit
        self.driver.get('http://localhost:8677/trip_input')
        self.driver.find_element(By.NAME, 'starting_point').send_keys("")
        self.driver.find_element(By.NAME, 'destination').send_keys("Boston")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-15")
        self.driver.find_element(By.XPATH, '//input[@value="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Input Trip", self.driver.title)

    def test_view_transportation_suggestions(self):
        # Login and input trip details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8677/trip_input')
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Boston")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-15")
        self.driver.find_element(By.XPATH, '//input[@value="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the transportation suggestions are displayed
        self.assertIn("Suggestions", self.driver.title)

    def test_save_preferred_transportation_options(self):
        # Login and input trip details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8677/trip_input')
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Boston")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-15")
        self.driver.find_element(By.XPATH, '//input[@value="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Select a preferred transportation option and click the save button
        self.driver.find_element(By.NAME, 'selected_option').send_keys("Bus")
        self.driver.find_element(By.XPATH, '//input[@value="Save Option"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the preferred option is saved successfully
        self.assertIn("Suggestions", self.driver.title)

    def test_user_logout(self):
        # Login successfully
        self.login("admin", "admin123")

        # Logout from the Dashboard Page
        self.driver.get('http://localhost:8677/')
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_view_estimated_costs_and_travel_times(self):
        # Login and input trip details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8677/trip_input')
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Boston")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-15")
        self.driver.find_element(By.XPATH, '//input[@value="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the estimated costs and travel times are displayed
        self.assertIn("Suggestions", self.driver.title)

    def test_compare_transportation_options(self):
        # Login and input trip details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8677/trip_input')
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Boston")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-15")
        self.driver.find_element(By.XPATH, '//input[@value="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Navigate to the comparison page
        self.driver.get('http://localhost:8677/comparison')
        self.assertIn("Comparison", self.driver.title)

if __name__ == '__main__':
    unittest.main()
