import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestVehicleMaintenanceTracker(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8562/')

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
        time.sleep(1)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message is displayed
        self.assertIn("already taken", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8562/')
        self.login("invalid_user", "invalid_pass")

        # Verify error message is displayed
        self.assertIn("incorrect", self.driver.page_source)

    def test_input_vehicle_information(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Navigate to the Vehicle Information Page
        self.driver.find_element(By.LINK_TEXT, 'Vehicle Information').click()
        time.sleep(1)

        # Enter valid vehicle information and submit the form
        self.driver.find_element(By.NAME, 'make').send_keys("Ford")
        self.driver.find_element(By.NAME, 'model').send_keys("Focus")
        self.driver.find_element(By.NAME, 'year').send_keys("2021")
        self.driver.find_element(By.NAME, 'mileage').send_keys("10000")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Verify confirmation message is displayed
        self.assertIn("saved successfully", self.driver.page_source)

        # Attempt to enter invalid vehicle information
        self.driver.find_element(By.NAME, 'mileage').clear()
        self.driver.find_element(By.NAME, 'mileage').send_keys("-10000")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Verify error message is displayed
        self.assertIn("invalid", self.driver.page_source)

    def test_track_regular_maintenance_tasks(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Navigate to the Maintenance Tracker Page
        self.driver.find_element(By.LINK_TEXT, 'Maintenance Tracking').click()
        time.sleep(1)

        # Enter a valid maintenance task and submit
        self.driver.find_element(By.NAME, 'vehicle_id').send_keys("1")
        self.driver.find_element(By.NAME, 'task').send_keys("Oil Change")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-10")
        self.driver.find_element(By.XPATH, '//button[text()="Add Maintenance Record"]').click()
        time.sleep(1)

        # Verify confirmation message is displayed
        self.assertIn("saved successfully", self.driver.page_source)

        # Attempt to add a maintenance task without specifying a task type
        self.driver.find_element(By.NAME, 'task').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Add Maintenance Record"]').click()
        time.sleep(1)

        # Verify error message is displayed
        self.assertIn("task type is required", self.driver.page_source)

    def test_send_reminders_and_notifications(self):
        # Functionality not implemented in the codebase
        self.fail("Functionality not implemented")

    def test_view_maintenance_history(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Navigate to the Maintenance History Page
        self.driver.find_element(By.LINK_TEXT, 'Maintenance History').click()
        time.sleep(1)

        # Verify the Maintenance History Page is displayed
        self.assertIn("Maintenance History", self.driver.title)

        # Check the maintenance history after adding a new maintenance record
        self.assertIn("Oil Change", self.driver.page_source)

    def test_update_or_delete_maintenance_records(self):
        # Functionality not implemented in the codebase
        self.fail("Functionality not implemented")

    def test_user_logout(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Click the logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Navigate to the Maintenance Tracker Page
        self.driver.find_element(By.LINK_TEXT, 'Maintenance Tracking').click()
        time.sleep(1)

        # Click the back button to return to the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)

        # Verify that the user is redirected back to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

    def test_view_and_update_vehicle_information(self):
        # Functionality not implemented in the codebase
        self.fail("Functionality not implemented")

if __name__ == '__main__':
    unittest.main()
