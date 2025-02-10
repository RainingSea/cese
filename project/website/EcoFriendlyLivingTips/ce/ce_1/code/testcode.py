import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestEcoFriendlyLivingTipsApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8624/')  # Access the login page

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

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

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
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_eco_friendly_tips(self):
        # Functionalities 5: Test viewing eco-friendly tips after logging in
        self.login("admin", "admin123")

        # Verify that the Home Page shows tips
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips), 0, "No eco-friendly tips found.")

    def test_submit_eco_friendly_tip(self):
        # Functionalities 5: Test submitting a new eco-friendly tip
        self.fail("Not implemented")

    def test_access_resources(self):
        # Functionalities 6: Test accessing resources page
        self.fail("Not implemented")

    def test_add_external_resource(self):
        # Functionalities 6: Test adding a new external resource
        self.fail("Not implemented")

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.fail("Not implemented")

    def test_profile_management(self):
        # Functionalities 8: Test profile management
        self.fail("Not implemented")

    def test_user_logout(self):
        # Functionalities 9: Test logging out
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_contact_support(self):
        # Functionalities 10: Test contacting support
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
