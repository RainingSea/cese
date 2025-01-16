import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMedicalInfoTracker(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8637/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register").click()

        # Verify the Registration Page is displayed
        self.assertIn("Registration", self.driver.title)

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register").click()
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify an error message is displayed (assuming an error message is shown on the same page)
        error_message = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("username is already taken", error_message)

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8637/')  # Navigate back to login page
        self.login("invalid_user", "wrong_password")

        # Verify an error message is displayed (assuming an error message is shown on the same page)
        error_message = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("credentials are incorrect", error_message)

    def test_manage_medical_information(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify the user can view their current medical information
        user_data = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("Flu", user_data)

        # Input new medical information and save (not implemented in the codebase)
        self.fail("Functionality not implemented")

    def test_set_and_receive_appointment_reminders(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify the user can view existing appointment reminders (not implemented in the codebase)
        self.fail("Functionality not implemented")

    def test_view_and_edit_medical_history(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify the user can view their complete medical history (not implemented in the codebase)
        self.fail("Functionality not implemented")

    def test_user_logout(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify the Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Click the logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify the user is logged out and redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8637/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
