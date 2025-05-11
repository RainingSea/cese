import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOfficeTaskFeedbackApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8476/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8476/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register with a new username
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify successful registration
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8476/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Registration failed", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Your Feedback Status", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8476/')  # Navigate back to login page
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Login failed", self.driver.page_source)

    def test_feedback_submission(self):
        # Functionality 3: Feedback Submission
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8476/submit_feedback')  # Navigate to feedback submission page
        self.assertIn("Submit Feedback", self.driver.title)

        # Submit feedback with valid details
        self.driver.find_element(By.NAME, 'content').send_keys("Great job on the project!")
        self.driver.find_element(By.NAME, 'category').send_keys("Positive")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify successful submission
        self.assertIn("Your Feedback Status", self.driver.title)

        # Attempt to submit feedback without filling in required fields
        self.driver.get('http://localhost:8476/submit_feedback')  # Navigate back to feedback submission page
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()  # Submit without filling
        self.assertIn("Feedback Content", self.driver.page_source)

    def test_feedback_review(self):
        # Functionality 5: Manager Review of Feedback
        self.login("admin", "admin123")  # Log in as manager
        self.driver.get('http://localhost:8476/feedback_review')  # Navigate to feedback review page
        self.assertIn("Feedback Review", self.driver.title)

    def test_view_feedback_status(self):
        # Functionality 6: View Feedback Status
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8476/status')  # Navigate to feedback status page
        self.assertIn("Your Feedback Status", self.driver.title)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Log in first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click the Logout button
        self.assertIn("Login", self.driver.title)

    def test_return_to_login_page(self):
        # Functionality 8: Return to Login Page
        self.login("admin", "admin123")  # Log in first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Logout
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()  # Click register link
        self.assertIn("Register", self.driver.title)

if __name__ == '__main__':
    unittest.main()
