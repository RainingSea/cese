import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOfficeTaskFeedbackApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8198/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8198/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8198/register')
        self.driver.find_element(By.NAME, 'username').send_keys("user1")  # Existing user
        self.driver.find_element(By.NAME, 'password').send_keys("test_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Check for error message (assuming the error message is displayed on the same page)
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("user1", "user123")  # Valid credentials
        self.assertIn("Feedback", self.driver.title)  # Assuming the title changes after login

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8198/')
        self.login("user1", "wrong_password")
        self.assertIn("Login", self.driver.title)  # Should still be on login page

    def test_feedback_submission(self):
        # Functionality 3: Feedback Submission
        self.login("user1", "user123")  # Log in first
        self.driver.get('http://localhost:8198/feedback')  # Navigate to feedback page
        self.assertIn("Submit Feedback", self.driver.title)

        # Submit feedback
        self.driver.find_element(By.NAME, 'feedback').send_keys("This is a feedback")
        self.driver.find_element(By.NAME, 'category').send_keys("General")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()

        # Verify redirection to status page
        self.assertIn("Feedback Status", self.driver.title)

    def test_view_feedback_status(self):
        # Functionality 6: View Feedback Status
        self.login("user1", "user123")  # Log in first
        self.driver.get('http://localhost:8198/status?username=user1')  # Navigate to status page
        self.assertIn("Feedback Status", self.driver.title)

        # Check if feedback is displayed
        self.assertIn("This is a feedback", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("user1", "user123")  # Log in first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Assuming there's a logout link
        self.assertIn("Login", self.driver.title)  # Verify redirection to login page

if __name__ == '__main__':
    unittest.main()
