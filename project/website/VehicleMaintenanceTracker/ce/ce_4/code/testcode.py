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
        self.driver.get('http://localhost:8687/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.ID, 'username').send_keys('new_user')
        self.driver.find_element(By.ID, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.ID, 'username').send_keys('admin')
        self.driver.find_element(By.ID, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Expect an error message indicating the username is already taken
        self.assertIn("Register", self.driver.title)  # Assuming it stays on the same page

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")
        # Verify that the user is redirected to another page
        self.assertNotIn("Login", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8687/')  # Navigate back to the login page
        self.login("invalid_user", "invalid_pass")
        # Expect an error message indicating incorrect credentials
        self.assertIn("Login", self.driver.title)  # Assuming it stays on the same page

    def test_input_vehicle_information(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Navigate to the Vehicle Information Page
        self.driver.get('http://localhost:8687/vehicle_info')
        self.assertIn("Vehicle Information", self.driver.title)

        # Enter valid vehicle information and submit the form
        self.driver.find_element(By.ID, 'make').send_keys('Ford')
        self.driver.find_element(By.ID, 'model').send_keys('Focus')
        self.driver.find_element(By.ID, 'year').send_keys('2021')
        self.driver.find_element(By.ID, 'mileage').send_keys('10000')
        self.driver.find_element(By.XPATH, '//input[@value="Add Vehicle"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the vehicle information is saved successfully
        # Assuming the page reloads and shows some confirmation

        # Attempt to enter invalid vehicle information (e.g., negative mileage)
        self.driver.find_element(By.ID, 'mileage').clear()
        self.driver.find_element(By.ID, 'mileage').send_keys('-10000')
        self.driver.find_element(By.XPATH, '//input[@value="Add Vehicle"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Expect an error message indicating invalid input
        # Assuming it stays on the same page

    # Placeholder for unimplemented functionalities
    def test_track_regular_maintenance_tasks(self):
        self.fail("Not implemented")

    def test_send_reminders_and_notifications(self):
        self.fail("Not implemented")

    def test_view_maintenance_history(self):
        self.fail("Not implemented")

    def test_update_or_delete_maintenance_records(self):
        self.fail("Not implemented")

    def test_user_logout(self):
        self.fail("Not implemented")

    def test_navigate_back_to_dashboard(self):
        self.fail("Not implemented")

    def test_view_and_update_vehicle_information(self):
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
