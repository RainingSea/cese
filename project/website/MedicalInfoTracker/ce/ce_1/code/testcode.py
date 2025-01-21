import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestMedicalInfoTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:9041/')  # Navigate to the login page

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
        self.assertIn("Registration", self.driver.title)

        # Enter a valid username and password, then submit the form
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

        # Verify an error message is displayed
        self.assertIn("username is already taken", self.driver.page_source)

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:9041/')  # Navigate back to the login page
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("credentials are incorrect", self.driver.page_source)

    def test_manage_medical_information(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify the user can view their current medical information
        self.assertIn("Your Medical Information", self.driver.page_source)

        # Input new medical information and save
        self.driver.find_element(By.NAME, 'diagnosis').send_keys("New Diagnosis")
        self.driver.find_element(By.NAME, 'medication').send_keys("New Medication")
        self.driver.find_element(By.NAME, 'treatment').send_keys("New Treatment")
        self.driver.find_element(By.XPATH, '//button[text()="Add Medical Info"]').click()
        time.sleep(1)  # Wait for the information to be saved

        # Verify the new information is displayed
        self.assertIn("New Diagnosis", self.driver.page_source)
        self.assertIn("New Medication", self.driver.page_source)
        self.assertIn("New Treatment", self.driver.page_source)

    def test_set_and_receive_appointment_reminders(self):
        # This functionality is not implemented in the codebase
        self.fail("Functionality not implemented")

    def test_view_and_edit_medical_history(self):
        # This functionality is not implemented in the codebase
        self.fail("Functionality not implemented")

    def test_user_logout(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify the Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Click the logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:9041/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
