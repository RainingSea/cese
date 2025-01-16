import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestVehicleMaintenanceTracker(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8686/')  # Navigate to the login page

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
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for existing username
        self.assertIn("Register", self.driver.title)  # Assuming the page reloads with an error

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("admin", "admin123")

        # Verify redirection to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8686/')  # Reload login page
        self.login("invalid_user", "invalid_pass")

        # Verify error message for invalid credentials
        self.assertIn("Login", self.driver.title)  # Assuming the page reloads with an error

    def test_input_vehicle_information(self):
        self.login("admin", "admin123")

        # Verify the Vehicle Information Page is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Enter valid vehicle information
        self.driver.find_element(By.NAME, 'make').send_keys("Toyota")
        self.driver.find_element(By.NAME, 'model').send_keys("Corolla")
        self.driver.find_element(By.NAME, 'year').send_keys("2020")
        self.driver.find_element(By.NAME, 'mileage').send_keys("15000")
        self.driver.find_element(By.XPATH, '//button[text()="Add Vehicle"]').click()
        time.sleep(1)  # Wait for the vehicle to be added

        # Verify the vehicle is added
        self.assertIn("Toyota Corolla (2020)", self.driver.page_source)

        # Attempt to enter invalid vehicle information
        self.driver.find_element(By.NAME, 'make').send_keys("Honda")
        self.driver.find_element(By.NAME, 'model').send_keys("Civic")
        self.driver.find_element(By.NAME, 'year').send_keys("2019")
        self.driver.find_element(By.NAME, 'mileage').send_keys("-5000")
        self.driver.find_element(By.XPATH, '//button[text()="Add Vehicle"]').click()
        time.sleep(1)  # Wait for the response

        # Verify error message for invalid input
        self.assertIn("Dashboard", self.driver.title)  # Assuming the page reloads with an error

    def test_track_regular_maintenance_tasks(self):
        self.fail("Functionality not implemented")

    def test_send_reminders_and_notifications(self):
        self.fail("Functionality not implemented")

    def test_view_maintenance_history(self):
        self.fail("Functionality not implemented")

    def test_update_or_delete_maintenance_records(self):
        self.fail("Functionality not implemented")

    def test_user_logout(self):
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        self.fail("Functionality not implemented")

    def test_view_and_update_vehicle_information(self):
        self.fail("Functionality not implemented")

if __name__ == '__main__':
    unittest.main()
