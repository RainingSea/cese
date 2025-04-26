import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOfficeTaskFeedbackApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8199/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the application process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.driver.find_element(By.NAME, 'username').send_keys("user1")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify an error message is displayed
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("user1", "user123")  # Valid credentials

        # Verify that the user is redirected to the feedback page
        self.assertIn("Submit Feedback", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8199/')  # Go back to login page
        self.login("user1", "wrong_password")  # Invalid password

        # Verify an error message is displayed
        self.assertIn("Login credentials are incorrect", self.driver.page_source)

    def test_feedback_submission(self):
        # Functionality 3: Feedback Submission
        self.login("user1", "user123")  # Log in successfully

        # Navigate to feedback submission page
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()

        # Fill in the feedback form
        self.driver.find_element(By.NAME, 'feedback').send_keys("This is a feedback")
        self.driver.find_element(By.NAME, 'category').send_keys("General")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify feedback submission confirmation
        self.assertIn("Feedback submitted successfully", self.driver.page_source)

        # Attempt to submit feedback without filling in required fields
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()  # Submit without filling

        # Verify an error message is displayed
        self.assertIn("All required fields must be filled", self.driver.page_source)

    def test_view_feedback_status(self):
        # Functionality 6: View Feedback Status
        self.login("user1", "user123")  # Log in successfully

        # Navigate to feedback status page
        self.driver.find_element(By.LINK_TEXT, 'View Feedback Status').click()

        # Verify that the user's feedback status is displayed
        self.assertIn("Pending", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("user1", "user123")  # Log in successfully

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate to the feedback page after logging out
        self.driver.get('http://localhost:8199/feedback')

        # Verify that the user is redirected back to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
