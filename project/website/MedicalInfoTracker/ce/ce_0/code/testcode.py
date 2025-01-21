import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestMedicalInfoTracker(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:9040/')

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

        # Verify Registration Page
        self.assertIn("Registration", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Check for error message
        self.assertIn("username is already taken", self.driver.page_source)

    def test_user_login(self):
        # Verify Login Page
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Invalid login
        self.driver.get('http://localhost:9040/')
        self.login("invalid_user", "invalid_pass")
        self.assertIn("credentials are incorrect", self.driver.page_source)

    def test_manage_medical_information(self):
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Add new medical information
        self.driver.find_element(By.NAME, 'diagnosis').send_keys("Cold")
        self.driver.find_element(By.NAME, 'medication').send_keys("Aspirin")
        self.driver.find_element(By.NAME, 'treatment').send_keys("Rest")
        self.driver.find_element(By.XPATH, '//button[text()="Add"]').click()
        time.sleep(1)

        # Verify new information is displayed
        self.assertIn("Cold", self.driver.page_source)

    def test_set_and_receive_appointment_reminders(self):
        self.fail("Functionality not implemented")

    def test_view_and_edit_medical_history(self):
        self.fail("Functionality not implemented")

    def test_user_logout(self):
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to access Dashboard after logout
        self.driver.get('http://localhost:9040/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
