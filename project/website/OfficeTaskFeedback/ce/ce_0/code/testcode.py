import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOfficeTaskFeedbackApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8362/') 

    def tearDown(self):
        # Close the web driver session and the subprocess
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
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that an error message is displayed
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify that the feedback submission page has loaded
        self.assertIn("Submit Feedback", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8362/')  # Go back to login page
        self.driver.find_element(By.NAME, 'username').send_keys("invalid_user")
        self.driver.find_element(By.NAME, 'password').send_keys("invalid_password")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that an error message is displayed
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_feedback_submission(self):
        # Functionality 3: Feedback Submission
        self.login("admin", "admin123")

        # Verify that the feedback submission form is displayed
        self.assertIn("Submit Feedback", self.driver.title)

        # Fill in the feedback form with valid details and submit it
        self.driver.find_element(By.NAME, 'feedback').send_keys("This is a test feedback.")
        self.driver.find_element(By.NAME, 'category').send_keys("General")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the feedback is submitted successfully
        self.assertIn("Feedback submitted successfully", self.driver.page_source)

        # Attempt to submit feedback without filling in required fields
        self.driver.find_element(By.NAME, 'feedback').clear()  # Clear feedback
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that an error message is displayed
        self.assertIn("All fields are required", self.driver.page_source)

    def test_feedback_categorization(self):
        # Functionality 4: Feedback Categorization
        self.login("admin", "admin123")

        # Verify that the feedback submission form is displayed
        self.assertIn("Submit Feedback", self.driver.title)

        # Select a category from the predefined categories dropdown
        self.driver.find_element(By.NAME, 'category').send_keys("Bug")
        self.driver.find_element(By.NAME, 'feedback').send_keys("This is a bug report.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the feedback is categorized correctly
        self.assertIn("Feedback submitted successfully", self.driver.page_source)

    def test_manager_review_feedback(self):
        # Functionality 5: Manager Review of Feedback
        self.login("admin", "admin123")

        # Navigate to the feedback review page
        self.driver.get('http://localhost:8362/review')
        time.sleep(1)  # Wait for the next page to load

        # Verify that feedback is displayed
        self.assertIn("Feedback Review", self.driver.title)
        self.assertGreater(len(self.driver.find_elements(By.TAG_NAME, 'tr')), 1, "No feedback found.")

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
