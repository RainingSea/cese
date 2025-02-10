import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestOfficeTaskFeedback(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start
        # Initialize the webdriver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8657/')

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
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

        # Verify that an error message is displayed
        self.assertIn("Register", self.driver.title)  # Assuming no redirection means error

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the user is redirected to the feedback page
        self.assertIn("Submit Feedback", self.driver.page_source)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8657/')
        self.login("invalid_user", "invalid_pass")

        # Verify that the login page is still displayed
        self.assertIn("Login", self.driver.title)

    def test_feedback_submission(self):
        # Log in successfully
        self.login("user1", "user123")

        # Verify that the feedback submission form is displayed
        self.assertIn("Submit Feedback", self.driver.page_source)

        # Fill in the feedback form with valid details and submit it
        self.driver.find_element(By.NAME, 'category').send_keys("General")
        self.driver.find_element(By.NAME, 'comment').send_keys("This is a test feedback.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the feedback page is still displayed
        self.assertIn("Submit Feedback", self.driver.page_source)

        # Attempt to submit feedback without filling in required fields
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the feedback page is still displayed
        self.assertIn("Submit Feedback", self.driver.page_source)

    def test_feedback_categorization(self):
        # Log in successfully
        self.login("user1", "user123")

        # Select a category from the predefined categories dropdown
        category_dropdown = self.driver.find_element(By.NAME, 'category')
        category_dropdown.send_keys("Suggestion")

        # Verify that the selected category is displayed correctly
        self.assertEqual(category_dropdown.get_attribute('value'), "Suggestion")

        # Submit feedback with a selected category
        self.driver.find_element(By.NAME, 'comment').send_keys("This is a suggestion.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the feedback page is still displayed
        self.assertIn("Submit Feedback", self.driver.page_source)

    def test_manager_review_of_feedback(self):
        # Log in as a manager
        self.login("admin", "admin123")

        # Navigate to the feedback review page
        self.driver.find_element(By.LINK_TEXT, 'Review Feedback').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that a list of submitted feedback is displayed
        self.assertIn("Feedback Review", self.driver.page_source)

    def test_view_feedback_status(self):
        # Log in successfully
        self.login("user1", "user123")

        # Navigate to the feedback review page
        self.driver.find_element(By.LINK_TEXT, 'Review Feedback').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that a list of the user's submitted feedback is displayed
        self.assertIn("Feedback Review", self.driver.page_source)

    def test_user_logout(self):
        # Log in successfully
        self.login("user1", "user123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_return_to_login_page(self):
        # Log in successfully
        self.login("user1", "user123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # On the Login Page, click the "Register" link
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Registration Page
        self.assertIn("Register", self.driver.title)

if __name__ == '__main__':
    unittest.main()
