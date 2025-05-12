import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOfficeTaskFeedbackApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8500/')  # Access the login page

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
        self.driver.get('http://localhost:8500/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8500/register')
        self.driver.find_element(By.NAME, 'username').send_keys("user1")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("test_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Feedback", self.driver.title)  # Check if redirected to feedback page

        self.driver.get('http://localhost:8500/')  # Navigate back to login page
        self.login("invalid_user", "admin123")  # Invalid username
        self.assertIn("Invalid credentials", self.driver.page_source)

        self.driver.get('http://localhost:8500/')  # Navigate back to login page
        self.login("admin", "wrong_password")  # Invalid password
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_feedback_submission(self):
        # Functionality 3: Feedback Submission
        self.login("user1", "user123")  # Log in
        self.driver.get('http://localhost:8500/feedback')  # Navigate to feedback page
        self.assertIn("Submit Feedback", self.driver.title)

        # Fill in the feedback form
        self.driver.find_element(By.NAME, 'comments').send_keys("Great job on the project!")
        self.driver.find_element(By.NAME, 'category').send_keys("General")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()

        # Verify feedback submission
        self.assertIn("Feedback Status", self.driver.title)

        # Attempt to submit feedback without filling in required fields
        self.driver.get('http://localhost:8500/feedback')
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()
        self.assertIn("All fields must be filled", self.driver.page_source)

    def test_feedback_status(self):
        # Functionality 6: View Feedback Status
        self.login("user1", "user123")  # Log in
        self.driver.get('http://localhost:8500/status')  # Navigate to status page
        self.assertIn("Feedback Status", self.driver.title)

        # Verify feedback status is displayed
        self.assertIn("Great job on the project!", self.driver.page_source)

    def test_manager_review(self):
        # Functionality 5: Manager Review of Feedback
        self.login("admin", "admin123")  # Log in as manager
        self.driver.get('http://localhost:8500/review')  # Navigate to review page
        self.assertIn("Review Feedback", self.driver.title)

        # Verify feedbacks are displayed
        self.assertIn("Great job on the project!", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Log in
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click logout
        self.assertIn("Login", self.driver.title)  # Verify redirected to login page

    def test_return_to_login_page(self):
        # Functionality 8: Return to Login Page
        self.login("admin", "admin123")  # Log in
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click logout
        self.driver.get('http://localhost:8500/')  # Navigate to login page
        self.assertIn("Login", self.driver.title)  # Verify login page is displayed

if __name__ == '__main__':
    unittest.main()
