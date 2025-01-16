import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestDailyHealthTipsApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8530/')

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
        # Verify that the Tips Page has loaded
        self.assertIn("Today's Health Tip", self.driver.page_source)

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
        # Functionalities 4: Test viewing the current daily health tip
        self.login("admin", "admin123")
        # Verify that the current daily health tip is displayed
        self.assertIn("Today's Health Tip", self.driver.page_source)

    def test_navigate_to_previous_or_next_tips(self):
        # Functionalities 5: Test navigating to previous or next tips
        self.login("admin", "admin123")
        # Click on the "Next Tip" button
        self.driver.find_element(By.XPATH, '//button[text()="Next Tip"]').click()
        time.sleep(1)
        # Verify that the next tip is displayed
        self.assertIn("Today's Health Tip", self.driver.page_source)
        # Click on the "Previous Tip" button
        self.driver.find_element(By.XPATH, '//button[text()="Previous Tip"]').click()
        time.sleep(1)
        # Verify that the previous tip is displayed
        self.assertIn("Today's Health Tip", self.driver.page_source)

    def test_view_historical_daily_health_tips_archive(self):
        # Functionalities 6: Test viewing historical daily health tips archive
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        time.sleep(1)
        # Verify that the archive page is displayed
        self.assertIn("Tips Archive", self.driver.title)

    def test_search_for_specific_tips_from_the_tips_archive(self):
        # Functionalities 7: Test searching for specific tips from the tips archive
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        time.sleep(1)
        search_query = "water"
        self.driver.find_element(By.NAME, 'search_query').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)
        # Verify that search results are displayed
        self.assertIn(search_query, self.driver.page_source)

    def test_submit_feedback_on_daily_health_tips(self):
        # Functionalities 8: Test submitting feedback on daily health tips
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()
        time.sleep(1)
        feedback_text = "Great tips!"
        self.driver.find_element(By.NAME, 'feedback').send_keys(feedback_text)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)
        # Verify that the feedback submission is successful
        self.assertIn("Today's Health Tip", self.driver.page_source)

    def test_data_storage_and_retrieval(self):
        # Functionalities 9: Test data storage and retrieval
        self.fail("Not implemented")

    def test_application_state_management(self):
        # Functionalities 10: Test application state management (logout)
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
