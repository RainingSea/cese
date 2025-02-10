import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestDailyHealthTipsApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8621/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Daily Health Tip Page has loaded
        self.assertIn("Daily Health Tip", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_current_daily_health_tip(self):
        # Functionalities 4: Test viewing the current daily health tip after logging in
        self.login("admin", "admin123")

        # Verify that the Daily Health Tip is displayed
        tip_content = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertIn("Stay hydrated!", tip_content)

    def test_navigate_to_previous_or_next_tips(self):
        # Functionalities 5: Test navigating to previous or next tips
        self.fail("Not implemented")

    def test_view_historical_daily_health_tips_archive(self):
        # Functionalities 6: Test viewing historical daily health tips archive
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()

        # Verify that the Archive Page has loaded with past tips
        self.assertIn("Archive of Health Tips", self.driver.title)

    def test_search_for_specific_tips_from_the_tips_archive(self):
        # Functionalities 7: Test searching for specific tips from the tips archive
        self.fail("Not implemented")

    def test_submit_feedback_on_daily_health_tips(self):
        # Functionalities 8: Test submitting feedback on daily health tips
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()

        # Enter feedback and submit
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'message').send_keys("Great tips!")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify feedback submission
        self.assertIn("Feedback", self.driver.title)

    def test_data_storage_and_retrieval(self):
        # Functionalities 9: Test data storage and retrieval
        self.fail("Not implemented")

    def test_application_state_management(self):
        # Functionalities 10: Test application state management (logout)
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
