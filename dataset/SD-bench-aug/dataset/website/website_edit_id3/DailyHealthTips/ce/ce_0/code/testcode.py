import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestDailyHealthTipsApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web app to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8123')

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
        self.assertIn("Daily Health Tip", self.driver.title)

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
        self.login("admin", "adminpass")

        # Verify that the Daily Health Tip is displayed
        tip = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertIn("Stay hydrated by drinking plenty of water throughout the day.", tip)

    def test_navigate_tips(self):
        # Functionalities 5: Test navigating to previous or next tips
        self.login("admin", "adminpass")

        # Click on the "Next Tip" button
        self.driver.find_element(By.XPATH, '//button[text()="Next Tip"]').click()
        time.sleep(1)  # Wait for the next tip to load

        # Verify the next tip is displayed
        next_tip = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertIn("Incorporate more fruits and vegetables into your meals.", next_tip)

        # Click on the "Previous Tip" button
        self.driver.find_element(By.XPATH, '//button[text()="Previous Tip"]').click()
        time.sleep(1)  # Wait for the previous tip to load

        # Verify the previous tip is displayed
        previous_tip = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertIn("Stay hydrated by drinking plenty of water throughout the day.", previous_tip)

    def test_view_historical_tips_archive(self):
        # Functionalities 6: Test viewing historical daily health tips archive
        self.login("admin", "adminpass")

        # Click on the "Archive" button
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        time.sleep(1)  # Wait for the archive page to load

        # Verify that the archive page displays all past tips
        archive_tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(archive_tips), 0, "No tips found in archive.")

    def test_search_tips(self):
        # Functionalities 7: Test searching for specific tips from the tips archive
        self.login("admin", "adminpass")

        # Navigate to Archive
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        time.sleep(1)  # Wait for the archive page to load

        # Enter a search term and submit
        self.driver.find_element(By.NAME, 'query').send_keys("exercise")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        # Verify that the search results contain the search term
        search_results = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertTrue(any("exercise" in tip.text.lower() for tip in search_results), "Search term not found in results.")

    def test_submit_feedback(self):
        # Functionalities 8: Test submitting feedback on daily health tips
        self.login("admin", "adminpass")

        # Navigate to Feedback
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()
        time.sleep(1)  # Wait for the feedback page to load

        # Enter feedback and submit
        feedback_text = "Great tips! Keep them coming."
        self.driver.find_element(By.NAME, 'feedback').send_keys(feedback_text)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()
        time.sleep(1)  # Wait for the feedback to be submitted

        # Verify that the feedback is displayed on the page
        feedback_list = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertTrue(any(feedback_text in feedback.text for feedback in feedback_list), "Feedback not found in list.")

    def test_data_storage(self):
        # Functionalities 9: Test data storage and retrieval
        self.fail("Not implemented")

    def test_application_state_management(self):
        # Functionalities 10: Test application state management (logout)
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
