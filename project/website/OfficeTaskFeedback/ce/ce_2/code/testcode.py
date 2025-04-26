import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestOfficeTaskFeedbackApp(unittest.TestCase):

    def setUp(self):
        # Start the server and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/')  # Replace 8000 with the actual port from main.py

    def tearDown(self):
        # Close the web driver session and terminate the server
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

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to log in with invalid credentials
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Log out to test invalid login
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Login credentials are incorrect", self.driver.page_source)

    def test_feedback_submission(self):
        # Functionality 3: Feedback Submission
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8000/feedback')  # Navigate to feedback page
        time.sleep(1)  # Wait for the next page to load

        # Fill in the feedback form
        self.driver.find_element(By.ID, 'content').send_keys("Great job on the project!")
        self.driver.find_element(By.ID, 'category').send_keys("Praise")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for submission confirmation

        # Verify feedback submission confirmation
        self.assertIn("Feedback submitted successfully", self.driver.page_source)

        # Attempt to submit feedback without filling in required fields
        self.driver.find_element(By.ID, 'content').clear()  # Clear content
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for error message

        # Verify error message for required fields
        self.assertIn("All required fields must be filled", self.driver.page_source)

    def test_feedback_categorization(self):
        # Functionality 4: Feedback Categorization
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8000/feedback')  # Navigate to feedback page
        time.sleep(1)  # Wait for the next page to load

        # Select a category and submit feedback
        self.driver.find_element(By.ID, 'category').send_keys("Request")
        self.driver.find_element(By.ID, 'content').send_keys("Need more resources for the team.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for submission confirmation

        # Verify feedback categorization
        self.assertIn("Feedback categorized successfully", self.driver.page_source)

    def test_view_feedback_status(self):
        # Functionality 6: View Feedback Status
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8000/feedback/status')  # Navigate to feedback status page
        time.sleep(1)  # Wait for the next page to load

        # Verify that the feedback status is displayed
        self.assertIn("Pending", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
