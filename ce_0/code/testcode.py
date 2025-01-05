import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestHealthTipsApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8082/') 

    def tearDown(self):
        # Close the web driver session and stop the application
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
        self.login("admin", "pass123")

        # Verify that the Tips Page has loaded
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

    def test_view_current_tip(self):
        # Functionalities 4: Test viewing current daily health tip after logging in
        self.login("admin", "pass123")

        # Verify that the current tip is displayed
        tip = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertTrue(tip, "No tip displayed.")

    def test_navigate_tips(self):
        # Functionalities 5: Test navigating to previous or next tips
        self.fail("Not implemented")  # No buttons for next/previous tips in the current implementation

    def test_view_archive(self):
        # Functionalities 6: Test viewing historical daily health tips archive
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the archive page is displayed
        self.assertIn("Tips Archive", self.driver.title)

    def test_search_tips(self):
        # Functionalities 7: Test searching for specific tips from the tips archive
        self.fail("Not implemented")  # No search functionality in the current implementation

    def test_submit_feedback(self):
        # Functionalities 8: Test submitting feedback on daily health tips
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()
        time.sleep(1)  # Wait for the next page to load

        feedback_text = "Great tips!"
        self.driver.find_element(By.NAME, 'feedback').send_keys(feedback_text)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the feedback to be submitted

        # Verify redirection to the tips page
        self.assertIn("Daily Health Tips", self.driver.title)

    def test_data_storage(self):
        # Functionalities 9: Test data storage and retrieval
        self.fail("Not implemented")  # No functionality to submit a new tip in the current implementation

    def test_logout(self):
        # Functionalities 10: Test application state management (logout)
        self.fail("Not implemented")  # No logout functionality in the current implementation

if __name__ == '__main__':
    unittest.main()
