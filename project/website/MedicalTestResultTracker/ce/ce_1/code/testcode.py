import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMedicalTestResultTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8183/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        # Input valid username and password for registration
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("user1")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_user_login(self):
        # Test valid login
        self.login("user1", "user123")
        self.assertIn("Dashboard", self.driver.title)

        # Test invalid login
        self.driver.get('http://localhost:8183/')  # Go back to login page
        self.login("user1", "wrongpassword")
        self.assertIn("Login", self.driver.title)  # Should still be on login page

    def test_input_and_manage_medical_test_results(self):
        # Log in successfully
        self.login("user1", "user123")
        self.assertIn("Dashboard", self.driver.title)

        # Input valid medical test results
        self.driver.find_element(By.NAME, 'test_name').send_keys("Blood Test")
        self.driver.find_element(By.NAME, 'result').send_keys("Normal")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-01")
        self.driver.find_element(By.XPATH, '//button[text()="Add Test Result"]').click()

        # Verify test result is saved
        self.assertIn("Blood Test: Normal", self.driver.page_source)

        # Attempt to input invalid test results (e.g., negative values)
        self.driver.find_element(By.NAME, 'test_name').send_keys("Invalid Test")
        self.driver.find_element(By.NAME, 'result').send_keys("-1")  # Invalid result
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-01")
        self.driver.find_element(By.XPATH, '//button[text()="Add Test Result"]').click()

        # Verify error message for invalid input
        self.assertIn("Invalid input", self.driver.page_source)

    def test_set_and_receive_reminders(self):
        # Log in successfully
        self.login("user1", "user123")
        self.assertIn("Dashboard", self.driver.title)

        # Navigate to Reminders Page
        self.driver.find_element(By.LINK_TEXT, 'View Reminders').click()

        # Set a reminder
        self.driver.find_element(By.NAME, 'reminder_text').send_keys("Follow up test")
        self.driver.find_element(By.NAME, 'date_time').send_keys("2023-10-10T10:00")
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()

        # Verify reminder is saved
        self.assertIn("Follow up test", self.driver.page_source)

    def test_user_logout(self):
        # Log in successfully
        self.login("user1", "user123")
        self.assertIn("Dashboard", self.driver.title)

        # Click the logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
