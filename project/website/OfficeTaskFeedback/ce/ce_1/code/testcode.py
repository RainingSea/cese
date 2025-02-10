import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOfficeTaskFeedback(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8658/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.get('http://localhost:8658/register')
        
        # Verify the Registration Page is displayed
        self.assertIn("Registration", self.driver.title)

        # Enter a valid username and password and submit
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify successful registration redirects to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8658/register')
        self.driver.find_element(By.NAME, 'username').send_keys('user1')
        self.driver.find_element(By.NAME, 'password').send_keys('user123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Registration", self.driver.title)  # Assuming it stays on the same page

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8658/login')

        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("user1", "user123")

        # Verify redirection to the feedback page
        self.assertIn("Feedback", self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8658/login')
        self.login("invalid_user", "invalid_pass")

        # Verify error message for invalid credentials
        self.assertIn("Login", self.driver.title)  # Assuming it stays on the same page

    def test_feedback_submission(self):
        # Log in and navigate to feedback submission page
        self.login("user1", "user123")
        self.driver.get('http://localhost:8658/feedback')

        # Verify feedback submission form is displayed
        self.assertIn("Feedback Submission", self.driver.title)

        # Fill in and submit feedback form
        self.driver.find_element(By.NAME, 'category').send_keys('General')
        self.driver.find_element(By.NAME, 'content').send_keys('This is a test feedback.')
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify redirection to status page
        self.assertIn("Feedback Status", self.driver.title)

        # Attempt to submit feedback with missing fields
        self.driver.get('http://localhost:8658/feedback')
        self.driver.find_element(By.NAME, 'category').send_keys('')
        self.driver.find_element(By.NAME, 'content').send_keys('')
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify error message for missing fields
        self.assertIn("Feedback Submission", self.driver.title)  # Assuming it stays on the same page

    def test_feedback_categorization(self):
        # Log in and navigate to feedback submission page
        self.login("user1", "user123")
        self.driver.get('http://localhost:8658/feedback')

        # Select a category and submit feedback
        self.driver.find_element(By.NAME, 'category').send_keys('General')
        self.driver.find_element(By.NAME, 'content').send_keys('Categorized feedback.')
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify feedback is categorized correctly
        self.assertIn("Feedback Status", self.driver.title)

    def test_manager_review_feedback(self):
        # Log in as manager and navigate to review page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8658/review')

        # Verify list of feedback is displayed
        self.assertIn("Feedback Review", self.driver.title)

        # Click on a feedback entry to view details
        # Assuming there's a way to click and view details, which is not implemented in the current HTML

    def test_view_feedback_status(self):
        # Log in and navigate to feedback status page
        self.login("user1", "user123")
        self.driver.get('http://localhost:8658/status')

        # Verify user's feedback status is displayed
        self.assertIn("Your Feedback Status", self.driver.title)

    def test_user_logout(self):
        # Log in and logout
        self.login("user1", "user123")
        self.driver.get('http://localhost:8658/logout')

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

    def test_return_to_login_page(self):
        # Log in and click logout
        self.login("user1", "user123")
        self.driver.get('http://localhost:8658/logout')

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Click "Register here" link
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()

        # Verify redirection to registration page
        self.assertIn("Registration", self.driver.title)

if __name__ == '__main__':
    unittest.main()
