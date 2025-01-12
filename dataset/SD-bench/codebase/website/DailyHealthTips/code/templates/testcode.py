import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestDailyHealthTipsApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8318/') 

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
        self.assertIn("Daily Health Tips", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.page_source)

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
        self.assertIn("Login", self.driver.page_source)

    def test_view_current_daily_health_tip(self):
        # Functionalities 4: Test viewing current daily health tip after logging in
        self.login("admin", "admin123")

        # Verify that the Daily Health Tips Page shows tips
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips), 0, "No daily health tips found.")

    def test_navigate_to_previous_or_next_tips(self):
        # Functionalities 5: Test navigating to previous or next tips
        self.fail("Not implemented")

    def test_view_historical_daily_health_tips_archive(self):
        # Functionalities 6: Test viewing historical daily health tips archive
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Archive Page shows historical tips
        archive_tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(archive_tips), 0, "No historical tips found.")

    def test_search_for_specific_tips_from_archive(self):
        # Functionalities 7: Test searching for specific tips from the archive
        self.fail("Not implemented")

    def test_submit_feedback_on_daily_health_tips(self):
        # Functionalities 8: Test submitting feedback on daily health tips
        self.driver.get('http://localhost:8318/feedback')
        self.driver.find_element(By.NAME, 'username').send_keys("user1")
        self.driver.find_element(By.NAME, 'message').send_keys("Great tips!")
        self.driver.find_element(By.XPATH, '//input[@value="Submit Feedback"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.page_source)

    def test_data_storage_and_retrieval(self):
        # Functionalities 9: Test data storage and retrieval
        self.fail("Not implemented")

    def test_application_state_management(self):
        # Functionalities 10: Test application state management (logout)
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
