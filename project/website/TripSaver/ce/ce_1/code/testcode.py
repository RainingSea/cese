import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTripSaverApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8275/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8275/register')
        
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8275/register')
        self.driver.find_element(By.NAME, 'username').send_keys("user1")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("some_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8275/')
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Trip Input Page
        self.assertIn("Input Trip Details", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8275/')
        self.login("admin", "wrong_password")
        
        # Verify error message for incorrect credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_input_trip_details(self):
        # Functionality 3: Input Trip Details
        self.login("user1", "user123")
        self.driver.get('http://localhost:8275/trip_input')

        # Verify Trip Input form is displayed
        self.assertIn("Input Trip Details", self.driver.title)

        # Fill in the trip details with valid information
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-01")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify redirection to results page
        self.assertIn("Transportation Options", self.driver.title)

        # Attempt to submit with empty fields
        self.driver.get('http://localhost:8275/trip_input')
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify error message for empty fields
        self.assertIn("All fields are required", self.driver.page_source)

    def test_view_transportation_suggestions(self):
        # Functionality 4: View Transportation Suggestions
        self.login("user1", "user123")
        self.driver.get('http://localhost:8275/trip_input')

        # Fill in trip details and submit
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-01")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify transportation options are displayed
        self.assertIn("Bus", self.driver.page_source)
        self.assertIn("Train", self.driver.page_source)

    def test_save_preferred_transportation_option(self):
        # Functionality 5: Save Preferred Transportation Options
        self.login("user1", "user123")
        self.driver.get('http://localhost:8275/trip_input')

        # Fill in trip details and submit
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-01")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Save a preferred option
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()

        # Verify confirmation message
        self.assertIn("Preferred option saved", self.driver.page_source)

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("user1", "user123")
        self.driver.get('http://localhost:8275/')  # Assuming this is the dashboard

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_view_estimated_costs_and_travel_times(self):
        # Functionality 7: View Estimated Costs and Travel Times
        self.login("user1", "user123")
        self.driver.get('http://localhost:8275/trip_input')

        # Fill in trip details and submit
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-01")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify estimated costs and travel times are displayed
        self.assertIn("Cost:", self.driver.page_source)
        self.assertIn("Time:", self.driver.page_source)

    def test_compare_transportation_options(self):
        # Functionality 8: Compare Transportation Options
        self.login("user1", "user123")
        self.driver.get('http://localhost:8275/trip_input')

        # Fill in trip details and submit
        self.driver.find_element(By.NAME, 'starting_point').send_keys("New York")
        self.driver.find_element(By.NAME, 'destination').send_keys("Los Angeles")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-01")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify comparison options are displayed
        self.assertIn("Compare Options", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
