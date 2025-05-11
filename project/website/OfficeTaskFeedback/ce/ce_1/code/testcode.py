import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOfficeTaskFeedbackApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8477/')  # Use the port from main.py

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
        self.driver.get('http://localhost:8477/register')  # Navigate to registration page
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
        self.driver.get('http://localhost:8477/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Registration failed. Username already exists.", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Feedback", self.driver.title)  # Check if redirected to feedback page

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8477/')
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Invalid username or password.", self.driver.page_source)

    def test_feedback_submission(self):
        # Functionality 3: Feedback Submission
        self.login("admin", "admin123")  # Log in successfully
        self.driver.get('http://localhost:8477/feedback')  # Navigate to feedback page
        self.assertIn("Submit Feedback", self.driver.title)

        # Fill in the feedback form and submit
        self.driver.find_element(By.NAME, 'category').send_keys("General")
        self.driver.find_element(By.NAME, 'content').send_keys("This is a test feedback.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify feedback submission
        self.assertIn("Feedback Status", self.driver.title)

        # Attempt to submit feedback without filling in required fields
        self.driver.get('http://localhost:8477/feedback')
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()  # Submit without filling
        self.assertIn("All required fields must be filled.", self.driver.page_source)

    def test_feedback_categorization(self):
        # Functionality 4: Feedback Categorization
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8477/feedback')
        self.assertIn("Submit Feedback", self.driver.title)

        # Check if categories are displayed correctly
        categories = self.driver.find_elements(By.NAME, 'category')
        self.assertGreater(len(categories), 0, "No categories found.")

    def test_review_feedback(self):
        # Functionality 5: Manager Review of Feedback
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8477/review')  # Navigate to review page
        self.assertIn("Feedback Review", self.driver.title)

        # Check if feedbacks are displayed
        feedbacks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(feedbacks), 0, "No feedbacks found.")

    def test_view_feedback_status(self):
        # Functionality 6: View Feedback Status
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8477/feedback_status')  # Navigate to feedback status page
        self.assertIn("Feedback Status", self.driver.title)

        # Check if user's feedback status is displayed
        status = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(status), 0, "No feedback status found.")

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click the Logout button
        self.assertIn("Login", self.driver.title)  # Verify redirection to login page

    def test_return_to_login_page(self):
        # Functionality 8: Return to Login Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Logout
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register here.").click()  # Go to register
        self.assertIn("Register", self.driver.title)  # Verify redirection to registration page

if __name__ == '__main__':
    unittest.main()
