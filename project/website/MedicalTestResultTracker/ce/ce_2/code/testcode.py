import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMedicalTestResultTracker(unittest.TestCase):

    def setUp(self):
        # Start the main application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the actual port from main.py

    def tearDown(self):
        # Close the web driver session and terminate the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:5000/login')  # Navigate to login page
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.get('http://localhost:5000/register')
        
        # Verify Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter valid username and password
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify registration success
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:5000/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Registration failed", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:5000/login')
        
        # Enter valid credentials
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to log in with invalid credentials
        self.driver.get('http://localhost:5000/login')
        self.login("admin", "wrongpassword")

        # Verify error message for invalid credentials
        self.assertIn("Login failed", self.driver.page_source)

    def test_manage_test_results(self):
        # Log in successfully
        self.login("admin", "admin123")
        
        # Navigate to the Test Results Page
        self.driver.get('http://localhost:5000/test_results')  # Assuming this is the correct URL

        # Add a valid test result
        self.driver.find_element(By.NAME, 'result').send_keys("Blood Test: Normal")
        self.driver.find_element(By.XPATH, '//button[text()="Add Result"]').click()

        # Verify success message
        self.assertIn("Test result added successfully", self.driver.page_source)

        # Attempt to add an invalid test result (e.g., negative value)
        self.driver.find_element(By.NAME, 'result').send_keys("-1")  # Invalid input
        self.driver.find_element(By.XPATH, '//button[text()="Add Result"]').click()

        # Verify error message for invalid input
        self.assertIn("Failed to add test result", self.driver.page_source)

    def test_set_and_view_reminders(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Navigate to the Reminders Page
        self.driver.get('http://localhost:5000/reminders')  # Assuming this is the correct URL

        # Set a reminder
        self.driver.find_element(By.NAME, 'reminder').send_keys("Follow up in 6 months")
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()

        # Verify success message
        self.assertIn("Reminder set successfully", self.driver.page_source)

        # Check reminders list
        reminders = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(reminders), 0, "No reminders found.")

    def test_user_logout(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
