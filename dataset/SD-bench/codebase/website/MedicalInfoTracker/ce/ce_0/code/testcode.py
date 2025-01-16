import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestMedicalInfoTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8635/')  # Navigate to the login page

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
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
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
        self.assertIn("Register", self.driver.title)  # Assuming it stays on the registration page

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8635/')  # Navigate back to login
        self.login("invalid_user", "wrong_password")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)  # Assuming it stays on the login page

    def test_manage_medical_information(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify the user can view their current medical information
        self.assertIn("Dashboard", self.driver.title)
        medical_info = self.driver.find_elements(By.XPATH, '//ul/li[contains(text(), "Diagnosis:")]')
        self.assertGreater(len(medical_info), 0, "No medical information found.")

        # Input new medical information (not implemented in the codebase)
        self.fail("Adding new medical information is not implemented")

    def test_set_and_receive_appointment_reminders(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify the user can view existing appointment reminders
        self.assertIn("Dashboard", self.driver.title)
        appointments = self.driver.find_elements(By.XPATH, '//ul/li[contains(text(), "Date:")]')
        self.assertGreater(len(appointments), 0, "No appointments found.")

        # Set a new appointment reminder (not implemented in the codebase)
        self.fail("Setting new appointment reminders is not implemented")

    def test_view_and_edit_medical_history(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify the user can view their complete medical history
        self.assertIn("Dashboard", self.driver.title)
        medical_history = self.driver.find_elements(By.XPATH, '//ul/li[contains(text(), "Diagnosis:")]')
        self.assertGreater(len(medical_history), 0, "No medical history found.")

        # Edit medical history (not implemented in the codebase)
        self.fail("Editing medical history is not implemented")

    def test_user_logout(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify the Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Click the logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is logged out and redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8635/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
