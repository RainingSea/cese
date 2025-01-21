import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestEcoFriendlyLivingApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:9031/')  # Access the login page

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

    def test_view_introduction(self):
        # Functionalities 4: Test viewing introduction to eco-friendly living
        self.fail("Not implemented")

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting eco-friendly living tips
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Tips').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Tips Page has loaded
        self.assertIn("Eco-Friendly Tips", self.driver.title)

        # Submit a new tip
        new_tip = "Use reusable bags"
        self.driver.find_element(By.NAME, 'content').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be added

        # Verify that the new tip is displayed
        self.assertIn(new_tip, self.driver.page_source)

    def test_access_and_add_resources(self):
        # Functionalities 6: Test accessing and adding external resources
        self.fail("Not implemented")

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Community Forum').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Forum Page has loaded
        self.assertIn("Community Forum", self.driver.title)

        # Submit a new forum post
        new_post = "What are your thoughts on solar energy?"
        self.driver.find_element(By.NAME, 'content').send_keys(new_post)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Post"]').click()
        time.sleep(1)  # Wait for the post to be added

        # Verify that the new post is displayed
        self.assertIn(new_post, self.driver.page_source)

    def test_profile_management(self):
        # Functionalities 8: Test profile management
        self.fail("Not implemented")

    def test_logout(self):
        # Functionalities 9: Test user logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_contact_support(self):
        # Functionalities 10: Test contact support
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Contact Us').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the contact form
        message = "I need help with my account."
        self.driver.find_element(By.NAME, 'message').send_keys(message)
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()
        time.sleep(1)  # Wait for the message to be sent

        # Verify that a confirmation message is displayed
        self.assertIn("Message sent successfully", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
