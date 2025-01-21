import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestEcoFriendlyLivingTipsApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:9028/') 

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

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

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
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_introduction(self):
        # Functionalities 4: Test viewing introduction to eco-friendly living
        self.fail("Not implemented")

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting eco-friendly living tips
        self.fail("Not implemented")

    def test_access_and_add_resources(self):
        # Functionalities 6: Test accessing and adding external resources
        self.fail("Not implemented")

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Go to Forum').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Forum Page has loaded
        self.assertIn("Community Forum", self.driver.title)

        # Submit a new forum post
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'content').send_keys("This is a test post.")
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        time.sleep(1)  # Wait for the post to be submitted

        # Verify that the new post appears in the forum
        self.assertIn("This is a test post.", self.driver.page_source)

    def test_profile_management(self):
        # Functionalities 8: Test profile management
        self.fail("Not implemented")

    def test_logout(self):
        # Functionalities 9: Test logging out
        self.fail("Not implemented")

    def test_contact_support(self):
        # Functionalities 10: Test contact support
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
