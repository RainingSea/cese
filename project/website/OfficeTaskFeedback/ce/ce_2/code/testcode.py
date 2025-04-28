import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOfficeTaskFeedbackApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8364/')  # Access the login page

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
        self.driver.get('http://localhost:8364/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8364/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8364/')
        self.login("admin", "wrongpassword")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_feedback_submission(self):
        # Functionality 3: Feedback Submission
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8364/feedback')  # Navigate to feedback submission page
        self.assertIn("Submit Feedback", self.driver.title)

        # Fill in the feedback form
        self.driver.find_element(By.NAME, 'feedback').send_keys("Great job on the project!")
        self.driver.find_element(By.NAME, 'category').send_keys("General")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()

        # Verify feedback submission
        self.assertIn("Feedback submitted successfully", self.driver.page_source)

        # Attempt to submit feedback without filling required fields
        self.driver.get('http://localhost:8364/feedback')
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()
        self.assertIn("All fields are required", self.driver.page_source)

    def test_feedback_categorization(self):
        # Functionality 4: Feedback Categorization
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8364/feedback')  # Navigate to feedback submission page

        # Select a category and submit feedback
        self.driver.find_element(By.NAME, 'feedback').send_keys("Need to improve response time.")
        self.driver.find_element(By.NAME, 'category').send_keys("Complaint")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()

        # Verify feedback categorization
        self.assertIn("Complaint", self.driver.page_source)

    def test_feedback_review(self):
        # Functionality 5: Manager Review of Feedback
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8364/feedback_review')  # Navigate to feedback review page
        self.assertIn("Feedback Review", self.driver.title)

        # Verify feedback entries are displayed
        feedback_entries = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(feedback_entries), 0, "No feedback entries found.")

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate to the Dashboard Page after logging out
        self.driver.get('http://localhost:8364/')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
