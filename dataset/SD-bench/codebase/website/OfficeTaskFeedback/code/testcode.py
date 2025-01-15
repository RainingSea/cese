import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOfficeTaskFeedback(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8662/')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page is displayed
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
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Feedback Page
        self.assertIn("Feedback", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8662/')
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)

    def test_feedback_submission(self):
        # Log in successfully and navigate to the feedback submission page
        self.login("admin", "admin123")
        self.assertIn("Feedback", self.driver.title)

        # Fill in the feedback form with valid details and submit it
        self.driver.find_element(By.NAME, 'content').send_keys("Great service!")
        self.driver.find_element(By.NAME, 'category').send_keys("Service")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the status page
        self.assertIn("Feedback Status", self.driver.title)

        # Attempt to submit feedback without filling in required fields
        self.driver.get('http://localhost:8662/feedback')
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Feedback", self.driver.title)

    def test_feedback_categorization(self):
        # Log in successfully and navigate to the feedback submission page
        self.login("admin", "admin123")
        self.assertIn("Feedback", self.driver.title)

        # Select a category and submit feedback
        self.driver.find_element(By.NAME, 'content').send_keys("Needs improvement.")
        self.driver.find_element(By.NAME, 'category').send_keys("Service")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the feedback is categorized correctly
        self.assertIn("Feedback Status", self.driver.title)

    def test_manager_review_of_feedback(self):
        # This functionality is not implemented in the codebase
        self.fail("Manager review of feedback functionality not implemented")

    def test_view_feedback_status(self):
        # Log in successfully and navigate to the feedback status page
        self.login("user1", "user123")
        self.driver.get('http://localhost:8662/status')
        self.assertIn("Feedback Status", self.driver.title)

        # Refresh the feedback status page after a manager updates the status
        # This part cannot be tested as manager functionality is not implemented

    def test_user_logout(self):
        # Log in and then log out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate to the Dashboard Page after logging out
        self.driver.get('http://localhost:8662/feedback')
        self.assertIn("Login", self.driver.title)

    def test_return_to_login_page(self):
        # Log in and then log out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # On the Login Page, click the "Register" link
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the Registration Page
        self.assertIn("Register", self.driver.title)

if __name__ == '__main__':
    unittest.main()
