import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestMedicalInfoTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:9043/') 

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
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

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)  # Assuming it stays on the same page

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:9043/')  # Go back to login page
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)  # Assuming it stays on the login page

    def test_manage_medical_information(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify the user can view their current medical information
        records = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(records), 0, "No medical records found.")

        # Input new medical information and save
        self.driver.find_element(By.NAME, 'diagnosis').send_keys("Test Diagnosis")
        self.driver.find_element(By.NAME, 'medication').send_keys("Test Medication")
        self.driver.find_element(By.NAME, 'treatment').send_keys("Test Treatment")
        self.driver.find_element(By.XPATH, '//button[text()="Add Record"]').click()
        time.sleep(1)  # Wait for the page to update

        # Verify the new information is displayed
        self.assertIn("Test Diagnosis", self.driver.page_source)

    def test_user_logout(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Click the logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:9043/dashboard')
        self.assertIn("Login", self.driver.title)  # Should redirect to login page

if __name__ == '__main__':
    unittest.main()
