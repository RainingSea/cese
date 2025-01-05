import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestDailyHealthTipsApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8015')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Daily Health Tips Page has loaded
        self.assertIn("Daily Health Tip", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_current_daily_health_tip(self):
        # Functionalities 4: Test viewing current daily health tip after logging in
        self.login("admin", "admin123")

        # Verify that the current daily health tip is displayed
        self.assertIn("Daily Health Tip", self.driver.page_source)

    def test_navigate_previous_next_tips(self):
        # Functionalities 5: Test navigating to previous or next tips
        self.login("admin", "admin123")

        # Click on the "Next Tip" button
        self.driver.find_element(By.LINK_TEXT, 'Next').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the next tip is displayed
        self.assertIn("Daily Health Tip", self.driver.page_source)

        # Click on the "Previous Tip" button
        self.driver.find_element(By.LINK_TEXT, 'Previous').click()
        time.sleep(1)  # Wait for the previous tip to load

        # Verify that the previous tip is displayed
        self.assertIn("Daily Health Tip", self.driver.page_source)

    def test_view_historical_tips_archive(self):
        # Functionalities 6: Test viewing historical daily health tips archive
        self.login("admin", "admin123")

        # Click on the "Archive" button
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        time.sleep(1)  # Wait for the archive page to load

        # Verify that the archive page is displayed with past tips
        self.assertIn("Archive of Historical Health Tips", self.driver.page_source)

    def test_submit_feedback(self):
        # Functionalities 8: Test submitting feedback on daily health tips
        self.login("admin", "admin123")

        # Navigate to Feedback Page
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()
        time.sleep(1)  # Wait for the feedback page to load

        feedback_text = "This is a test feedback."

        # Submit feedback
        self.driver.find_element(By.NAME, 'feedback').send_keys(feedback_text)
        self.driver.find_element(By.XPATH, '//input[@value="Submit"]').click()
        time.sleep(1)  # Wait for the feedback to be submitted

        # Verify that the feedback submission is successful
        self.assertIn("Daily Health Tip", self.driver.page_source)

    def test_application_state_management(self):
        # Functionalities 10: Test logging out
        self.login("admin", "admin123")

        # Click the Logout button (assuming there's a logout button)
        # self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        # time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        # self.assertIn("Login", self.driver.title)
        self.fail("Logout functionality not implemented")

if __name__ == '__main__':
    unittest.main()
