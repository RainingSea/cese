import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOfficeTaskFeedbackApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8542/')

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
        # Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password and submit
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        error_message = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertIn("Username already exists", error_message)

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "admin123")

        # Verify redirection to the feedback submission page
        self.assertIn("Submit Feedback", self.driver.title)

        # Test invalid login
        self.driver.get('http://localhost:8542/')
        self.login("invalid_user", "wrong_password")

        # Verify redirection back to login page
        self.assertIn("Login", self.driver.title)

    def test_feedback_submission(self):
        # Test feedback submission functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()
        time.sleep(1)

        # Verify feedback submission form is displayed
        self.assertIn("Submit Feedback", self.driver.title)

        # Fill in the feedback form and submit
        self.driver.find_element(By.NAME, 'feedback_text').send_keys("Great work!")
        self.driver.find_element(By.NAME, 'category').send_keys("Project")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Verify redirection to feedback review page
        self.assertIn("Feedback Review", self.driver.title)

        # Attempt to submit feedback without filling required fields
        self.driver.find_element(By.LINK_TEXT, 'Submit More Feedback').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Verify error message for missing fields
        error_message = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertIn("all required fields must be filled", error_message)

    def test_feedback_categorization(self):
        # Test feedback categorization functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()
        time.sleep(1)

        # Select a category and submit feedback
        self.driver.find_element(By.NAME, 'feedback_text').send_keys("Need more resources.")
        self.driver.find_element(By.NAME, 'category').send_keys("Resources")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Verify feedback is categorized correctly
        feedback_list = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertTrue(any("Resources" in feedback.text for feedback in feedback_list))

    def test_manager_review_of_feedback(self):
        # Test manager review of feedback functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Feedback Review').click()
        time.sleep(1)

        # Verify list of feedback is displayed
        feedback_list = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(feedback_list), 0)

        # Click on a feedback entry to view details
        feedback_list[0].click()
        time.sleep(1)

        # Verify details of the selected feedback are displayed
        feedback_details = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("Status", feedback_details)

    def test_view_feedback_status(self):
        # Test view feedback status functionality
        self.fail("not implemented")

    def test_user_logout(self):
        # Test user logout functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate to the feedback submission page after logout
        self.driver.get('http://localhost:8542/submit_feedback')
        time.sleep(1)

        # Verify redirection back to the login page
        self.assertIn("Login", self.driver.title)

    def test_return_to_login_page(self):
        # Test return to login page functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Click the "Register" link
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)

        # Verify redirection to the registration page
        self.assertIn("Register", self.driver.title)

if __name__ == '__main__':
    unittest.main()
