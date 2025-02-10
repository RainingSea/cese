import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestOfficeTaskFeedback(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        # Initialize the webdriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8659/')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        # Terminate the application
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Create an account').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password and submit the registration form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Create an account').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8659/')
        time.sleep(1)  # Wait for the page to load

        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify the user is redirected to the Feedback Page
        self.assertIn("Feedback", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8659/')
        self.login("invalid_user", "wrong_password")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)

    def test_feedback_submission(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Navigate to the feedback submission page
        self.driver.get('http://localhost:8659/feedback')
        time.sleep(1)  # Wait for the page to load

        # Verify the feedback submission form is displayed
        self.assertIn("Feedback", self.driver.title)

        # Fill in the feedback form with valid details and submit it
        self.driver.find_element(By.NAME, 'feedback').send_keys("This is a test feedback.")
        self.driver.find_element(By.NAME, 'category').send_keys("Test Category")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the status page
        self.assertIn("Feedback Status", self.driver.title)

        # Attempt to submit feedback without filling in required fields
        self.driver.get('http://localhost:8659/feedback')
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Feedback", self.driver.title)

    def test_feedback_categorization(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Navigate to the feedback submission page
        self.driver.get('http://localhost:8659/feedback')
        time.sleep(1)  # Wait for the page to load

        # Select a category and submit feedback
        self.driver.find_element(By.NAME, 'feedback').send_keys("Feedback with category.")
        self.driver.find_element(By.NAME, 'category').send_keys("General")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the feedback is categorized correctly
        self.assertIn("Feedback Status", self.driver.title)

    def test_manager_review_of_feedback(self):
        # Log in as a manager
        self.login("admin", "admin123")

        # Navigate to the feedback review page
        self.driver.get('http://localhost:8659/status')
        time.sleep(1)  # Wait for the page to load

        # Verify a list of submitted feedback is displayed
        feedback_list = self.driver.find_elements(By.TAG_NAME, 'tr')
        self.assertGreater(len(feedback_list), 1, "No feedback entries found.")

    def test_view_feedback_status(self):
        # Log in successfully
        self.login("user1", "user123")

        # Navigate to the feedback status page
        self.driver.get('http://localhost:8659/status')
        time.sleep(1)  # Wait for the page to load

        # Verify a list of the user's submitted feedback is displayed
        feedback_list = self.driver.find_elements(By.TAG_NAME, 'tr')
        self.assertGreater(len(feedback_list), 1, "No feedback entries found.")

    def test_user_logout(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_return_to_login_page(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # On the Login Page, click the "Register here" link
        self.driver.find_element(By.LINK_TEXT, 'Create an account').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the Registration Page
        self.assertIn("Register", self.driver.title)

if __name__ == '__main__':
    unittest.main()
