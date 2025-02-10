import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestVehicleMaintenanceTracker(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8683/')

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
        self.assertIn("Registration", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Expectation: Error message for existing username
        self.assertIn("Registration", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")
        self.assertIn("Vehicle Information", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8683/')
        self.login("invalid_user", "wrong_password")
        self.assertIn("Login", self.driver.title)

    def test_input_vehicle_information(self):
        # Log in successfully and navigate to the Vehicle Information Page
        self.login("admin", "admin123")
        self.assertIn("Vehicle Information", self.driver.title)

        # Enter valid vehicle information and submit the form
        self.driver.find_element(By.NAME, 'make').send_keys("Ford")
        self.driver.find_element(By.NAME, 'model').send_keys("Focus")
        self.driver.find_element(By.NAME, 'year').send_keys("2021")
        self.driver.find_element(By.NAME, 'mileage').send_keys("10000")
        self.driver.find_element(By.XPATH, '//button[text()="Add Vehicle"]').click()
        time.sleep(1)

        # Expectation: Redirect to Maintenance Tracking Page
        self.assertIn("Maintenance Tracking", self.driver.title)

    def test_track_regular_maintenance_tasks(self):
        # Log in successfully and navigate to the Maintenance Tracker Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Maintenance Tracking').click()
        self.assertIn("Maintenance Tracking", self.driver.title)

        # Enter a valid maintenance task
        # Note: The current implementation does not support adding tasks directly from the UI
        self.fail("Adding maintenance tasks is not implemented in the UI")

    def test_view_maintenance_history(self):
        # Log in successfully and navigate to the Maintenance History Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Maintenance History').click()
        self.assertIn("Maintenance History", self.driver.title)

    def test_user_logout(self):
        # Log in successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Vehicle Information", self.driver.title)

        # Click the logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
