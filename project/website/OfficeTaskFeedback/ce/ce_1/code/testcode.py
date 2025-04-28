import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOfficeTaskFeedbackApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8363/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8363/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify successful registration
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8363/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Registration failed", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Feedback", self.driver.title)  # Check if redirected to the feedback page

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8363/')
        self.login("invalid_user", "invalid_password")
        self.assertIn("Login", self.driver.title)  # Check if still on login page

    def test_feedback_submission(self):
        # Functionality 3: Feedback Submission
        self.login("user1", "user123")  # Log in with valid user
        self.driver.get('http://localhost:8363/feedback')  # Navigate to feedback page
        self.assertIn("Submit Feedback", self.driver.title)

        # Submit feedback
        self.driver.find_element(By.NAME, 'username').send_keys("user1")
        self.driver.find_element(By.NAME, 'category').send_keys("General")
        self.driver.find_element(By.NAME, 'feedback').send_keys("This is a test feedback.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()

        # Verify feedback submission success
        self.assertIn("Feedback submitted successfully!", self.driver.page_source)

        # Attempt to submit feedback without filling required fields
        self.driver.find_element(By.NAME, 'feedback').clear()  # Clear feedback field
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()
        self.assertIn("all required fields must be filled", self.driver.page_source)

    def test_feedback_review(self):
        # Functionality 5: Manager Review of Feedback
        self.login("admin", "admin123")  # Log in as manager
        self.driver.get('http://localhost:8363/review')  # Navigate to feedback review page
        self.assertIn("Feedback Review", self.driver.title)

        # Verify feedback entries are displayed
        feedbacks = self.driver.find_elements(By.TAG_NAME, 'tr')
        self.assertGreater(len(feedbacks), 0, "No feedback entries found.")

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Log in
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click logout
        self.assertIn("Login", self.driver.title)  # Verify redirection to login page

if __name__ == '__main__':
    unittest.main()
