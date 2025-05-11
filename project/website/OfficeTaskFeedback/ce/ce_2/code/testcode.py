import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOfficeTaskFeedbackApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8478/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8478/register')  # Navigate to the Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check for success message
        self.assertIn("Registration successful!", self.driver.page_source)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8478/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check for error message
        self.assertIn("Registration failed. Username already exists.", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("user1", "user123")  # Valid credentials
        self.assertIn("Submit Feedback", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8478/')
        self.login("user1", "wrong_password")
        self.assertIn("Login failed. Please check your username and password.", self.driver.page_source)

    def test_feedback_submission(self):
        # Functionality 3: Feedback Submission
        self.login("user1", "user123")  # Log in first
        self.driver.get('http://localhost:8478/submit_feedback')  # Navigate to feedback submission page
        self.assertIn("Submit Feedback", self.driver.title)

        # Submit valid feedback
        self.driver.find_element(By.NAME, 'feedback').send_keys("Great service!")
        self.driver.find_element(By.NAME, 'category').send_keys("General")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check for confirmation message
        self.assertIn("Your feedback has been submitted.", self.driver.page_source)

        # Attempt to submit feedback without filling in required fields
        self.driver.get('http://localhost:8478/submit_feedback')
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check for error message
        self.assertIn("All required fields must be filled.", self.driver.page_source)

    def test_feedback_categorization(self):
        # Functionality 4: Feedback Categorization
        self.login("user1", "user123")  # Log in first
        self.driver.get('http://localhost:8478/submit_feedback')  # Navigate to feedback submission page
        self.assertIn("Submit Feedback", self.driver.title)

        # Check if categories are displayed
        categories = self.driver.find_elements(By.TAG_NAME, 'option')
        self.assertGreater(len(categories), 0, "No categories found.")

        # Submit feedback with a selected category
        self.driver.find_element(By.NAME, 'feedback').send_keys("Need more options.")
        self.driver.find_element(By.NAME, 'category').send_keys("Suggestion")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check for confirmation message
        self.assertIn("Your feedback has been submitted.", self.driver.page_source)

    def test_manager_review_feedback(self):
        # Functionality 5: Manager Review of Feedback
        self.login("admin", "admin123")  # Log in as manager
        self.driver.get('http://localhost:8478/feedback_review')  # Navigate to feedback review page
        self.assertIn("Feedback Review", self.driver.title)

        # Check if feedbacks are displayed
        feedbacks = self.driver.find_elements(By.TAG_NAME, 'tr')
        self.assertGreater(len(feedbacks), 1, "No feedbacks found for review.")

    def test_view_feedback_status(self):
        # Functionality 6: View Feedback Status
        self.login("user1", "user123")  # Log in first
        self.driver.get('http://localhost:8478/status_display')  # Navigate to status display page
        self.assertIn("Your Feedback Status", self.driver.title)

        # Check if user's feedback status is displayed
        statuses = self.driver.find_elements(By.TAG_NAME, 'tr')
        self.assertGreater(len(statuses), 1, "No feedback statuses found.")

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("user1", "user123")  # Log in first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_return_to_login_page(self):
        # Functionality 8: Return to Login Page
        self.login("user1", "user123")  # Log in first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

if __name__ == '__main__':
    unittest.main()
