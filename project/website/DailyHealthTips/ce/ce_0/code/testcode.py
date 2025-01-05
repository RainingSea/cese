import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestDailyHealthTipsApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8014')

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

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "adminpass")

        # Verify that the Daily Health Tips Page has loaded
        self.assertIn("Daily Health Tips", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
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

    def test_view_current_daily_health_tip(self):
        # Functionalities 4: Test viewing current daily health tip after logging in
        self.login("admin", "adminpass")

        # Verify that the current daily health tip is displayed
        tip = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertTrue(tip, "No daily health tip displayed.")

    def test_navigate_tips(self):
        # Functionalities 5: Test navigating to previous or next tips
        self.login("admin", "adminpass")

        # Click on the "Next Tip" button
        self.driver.find_element(By.LINK_TEXT, 'Next').click()
        time.sleep(1)  # Wait for the next tip to load

        # Verify that the next daily health tip is displayed
        next_tip = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertTrue(next_tip, "Next daily health tip not displayed.")

        # Click on the "Previous Tip" button
        self.driver.find_element(By.LINK_TEXT, 'Previous').click()
        time.sleep(1)  # Wait for the previous tip to load

        # Verify that the previous daily health tip is displayed
        previous_tip = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertTrue(previous_tip, "Previous daily health tip not displayed.")

    def test_view_historical_tips_archive(self):
        # Functionalities 6: Test viewing historical daily health tips archive
        self.login("admin", "adminpass")

        # Click on the "Archive" button
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        time.sleep(1)  # Wait for the archive page to load

        # Verify that the historical tips archive is displayed
        archive = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(archive), 0, "No historical tips found in the archive.")

    def test_submit_feedback(self):
        # Functionalities 8: Test submitting feedback on daily health tips
        self.login("admin", "adminpass")

        # Navigate to Feedback Page
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()
        time.sleep(1)  # Wait for the feedback page to load

        feedback_text = "Great tips, very helpful!"

        # Fill out the feedback form
        self.driver.find_element(By.NAME, 'feedback').send_keys(feedback_text)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()
        time.sleep(1)  # Wait for the feedback to be submitted

        # Verify that the feedback submission is successful
        self.assertIn("Feedback", self.driver.title)

    def test_application_state_management(self):
        # Functionalities 10: Test logging out
        self.login("admin", "adminpass")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
