import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestDailyHealthTipsApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8356/')  # Open the login page

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
        self.login("admin", "admin123")

        # Verify that the Daily Health Tips Page has loaded
        self.assertIn("Today's Health Tip", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
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

    def test_view_current_daily_health_tip(self):
        # Functionalities 4: Test viewing current daily health tip after logging in
        self.login("admin", "admin123")

        # Verify that the Daily Health Tip is displayed
        self.assertIn("Today's Health Tip", self.driver.page_source)

    def test_navigate_to_previous_or_next_tips(self):
        # Functionalities 5: Test navigation to previous or next tips
        self.login("admin", "admin123")

        # Attempt to navigate to the next tip (not implemented in the codebase)
        self.fail("Next Tip functionality not implemented")

    def test_view_historical_daily_health_tips_archive(self):
        # Functionalities 6: Test viewing historical daily health tips archive
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Tips Archive is displayed
        self.assertIn("Health Tips Archive", self.driver.page_source)

    def test_search_for_specific_tips_from_the_tips_archive(self):
        # Functionalities 7: Test searching for specific tips from the tips archive
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        time.sleep(1)  # Wait for the next page to load

        # Perform a search
        self.driver.find_element(By.NAME, 'query').send_keys("water")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results

        # Verify that the search results are displayed
        self.assertIn("Stay hydrated by drinking at least 8 glasses of water a day.", self.driver.page_source)

    def test_submit_feedback_on_daily_health_tips(self):
        # Functionalities 8: Test submitting feedback on daily health tips
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()
        time.sleep(1)  # Wait for the next page to load

        # Submit feedback
        self.driver.find_element(By.NAME, 'feedback').send_keys("Great tips, very helpful!")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the feedback submission

        # Verify that the feedback submission redirects back to the Daily Tip page
        self.assertIn("Today's Health Tip", self.driver.page_source)

    def test_data_storage_and_retrieval(self):
        # Functionalities 9: Test data storage and retrieval (not implemented in the codebase)
        self.fail("Data storage and retrieval functionality not implemented")

    def test_application_state_management(self):
        # Functionalities 10: Test application state management (logout)
        self.login("admin", "admin123")

        # Attempt to log out (not implemented in the codebase)
        self.fail("Logout functionality not implemented")

if __name__ == '__main__':
    unittest.main()
