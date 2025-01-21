import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestCultureFactsApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server a second to start

        # Initialize the webdriver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:9017/')

    def tearDown(self):
        # Close the web driver session and stop the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)

        # Verify Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        self.driver.find_element(By.ID, 'username').send_keys('new_user')
        self.driver.find_element(By.ID, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'username').send_keys('user1')
        self.driver.find_element(By.ID, 'password').send_keys('user123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Check for error message
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Verify Login Page
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login('admin', 'admin123')
        self.assertIn("Dashboard", self.driver.title)

        # Invalid login
        self.driver.get('http://localhost:9017/')
        self.login('admin', 'wrongpassword')
        self.assertIn("Login", self.driver.title)

    def test_explore_cultures_on_dashboard(self):
        self.login('admin', 'admin123')
        self.assertIn("Dashboard", self.driver.title)

        # Check for list of cultures
        cultures = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cultures), 0)

        # Click on a culture
        cultures[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)
        self.assertIn("Culture Details", self.driver.title)

    def test_view_culture_details(self):
        self.login('admin', 'admin123')
        self.driver.find_element(By.LINK_TEXT, 'Japanese').click()
        time.sleep(1)

        # Verify Culture Details Page
        self.assertIn("Culture Details", self.driver.title)
        self.assertIn("Rich in traditions", self.driver.page_source)

    def test_search_cultures_or_facts(self):
        self.fail("Not implemented")

    def test_bookmark_culture_facts(self):
        self.fail("Not implemented")

    def test_view_and_manage_bookmarks(self):
        self.fail("Not implemented")

    def test_user_logout(self):
        self.login('admin', 'admin123')
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to Login Page
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
