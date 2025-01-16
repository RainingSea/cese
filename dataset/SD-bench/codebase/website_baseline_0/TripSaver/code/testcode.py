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
        self.driver.get('http://localhost:8561/')

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

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify registration success message
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("Username already exists", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify redirection to the Trip Input Page
        self.assertIn("Trip Input", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8561/')
        self.login("invalid_user", "invalid_pass")

        # Verify error message for incorrect credentials
        self.assertIn("Invalid username or password", self.driver.page_source)

    def test_input_trip_details(self):
        # Login and navigate to the Trip Details input page
        self.login("admin", "admin123")
        self.assertIn("Trip Input", self.driver.title)

        # Fill in the trip details with valid information and submit
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-01")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Verify redirection to the Suggestions Page
        self.assertIn("Suggestions", self.driver.title)

        # Leave one or more fields empty and attempt to submit
        self.driver.get('http://localhost:8561/trip_input')
        self.driver.find_element(By.NAME, 'starting_point').send_keys("")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-01")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Verify error message for empty fields
        self.assertIn("All fields are required", self.driver.page_source)

    def test_view_transportation_suggestions(self):
        # Login and input trip details
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-01")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Verify transportation suggestions are displayed
        self.assertIn("Bus", self.driver.page_source)
        self.assertIn("Train", self.driver.page_source)
        self.assertIn("Car", self.driver.page_source)

    def test_save_preferred_transportation_options(self):
        # Login and input trip details
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-01")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Select a preferred transportation option and save
        self.driver.find_element(By.LINK_TEXT, 'Back').click()
        self.driver.find_element(By.LINK_TEXT, 'Saved Options').click()
        self.driver.find_element(By.XPATH, '//option[text()="Bus"]').click()
        self.driver.find_element(By.XPATH, '//button[text()="Save Options"]').click()
        time.sleep(1)

        # Verify confirmation message
        self.assertIn("Options saved successfully", self.driver.page_source)

        # Navigate to the saved options page
        self.driver.find_element(By.LINK_TEXT, 'Saved Options').click()
        time.sleep(1)

        # Verify saved options are displayed
        self.assertIn("Bus", self.driver.page_source)

    def test_user_logout(self):
        # Login and logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Trip Input Page after logging out
        self.driver.get('http://localhost:8561/trip_input')
        self.assertIn("Login", self.driver.title)

    def test_view_estimated_costs_and_travel_times(self):
        # Login and input trip details
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-01")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Verify estimated costs and travel times are displayed
        self.assertIn("Cost: $20", self.driver.page_source)
        self.assertIn("Time: 2 hours", self.driver.page_source)

    def test_compare_transportation_options(self):
        # Login and input trip details
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'travel_date').send_keys("2023-12-01")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Navigate to the comparison page
        self.driver.find_element(By.LINK_TEXT, 'Back').click()
        self.driver.find_element(By.LINK_TEXT, 'Comparison').click()
        time.sleep(1)

        # Verify comparison view is displayed
        self.assertIn("Compare Transportation Options", self.driver.title)

if __name__ == '__main__':
    unittest.main()
