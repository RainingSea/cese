import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestDailyHealthTipsApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8317/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Today's Health Tip", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
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
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_current_daily_health_tip(self):
        # Functionalities 4: Test viewing current daily health tip after logging in
        self.login("admin", "admin123")
        self.assertIn("Today's Health Tip", self.driver.page_source)

    def test_submit_feedback(self):
        # Functionalities 8: Test submitting feedback on daily health tips
        self.login("admin", "admin123")
        feedback_text = "Great tips!"
        self.driver.find_element(By.NAME, 'feedback').send_keys(feedback_text)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()
        time.sleep(1)  # Wait for the feedback to be processed
        self.assertIn("Today's Health Tip", self.driver.page_source)

    def test_view_historical_tips_archive(self):
        # Functionalities 6: Test viewing historical tips archive
        self.login("admin", "admin123")
        # Assuming there's an Archive button to click
        # self.driver.find_element(By.LINK_TEXT, 'Archive').click()
        # time.sleep(1)  # Wait for the next page to load
        # self.assertIn("Historical Tips", self.driver.page_source)
        self.fail("Archive functionality not implemented")

    def test_search_tips(self):
        # Functionalities 7: Test searching for specific tips
        self.login("admin", "admin123")
        search_term = "water"
        search_box = self.driver.find_element(By.NAME, 'search')
        search_box.send_keys(search_term)
        search_box.submit()
        time.sleep(1)  # Wait for the search results to load
        self.assertIn("Stay hydrated by drinking plenty of water.", self.driver.page_source)

    def test_logout(self):
        # Functionalities 10: Test logging out
        self.login("admin", "admin123")
        # Assuming there's a Logout button to click
        # self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        # time.sleep(1)  # Wait for the next page to load
        # self.assertIn("Login", self.driver.title)
        self.fail("Logout functionality not implemented")

if __name__ == '__main__':
    unittest.main()
