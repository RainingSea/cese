import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestGreenLivingGuide(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8170/')  # Access the login page

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
        self.login("user1", "password1")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Login", self.driver.title)  # Registration redirects to login

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

    def test_view_sustainable_living_intro(self):
        # Functionalities 4: Test viewing sustainable living introduction
        self.login("user1", "password1")

        # Verify that the Dashboard Page shows the introduction
        self.assertIn("Welcome to the Dashboard", self.driver.page_source)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify tips are displayed
        self.assertIn("Sustainable Living Tips", self.driver.page_source)

        # Submit a new tip
        new_tip = "Use solar panels"
        self.driver.find_element(By.NAME, 'tip').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the tip to be saved

        # Verify the new tip is displayed
        self.assertIn(new_tip, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify articles are displayed
        self.assertIn("Articles on Sustainable Living", self.driver.page_source)

        # Submit a new article
        new_title = "New Article"
        new_content = "This is a new article about sustainability."
        self.driver.find_element(By.NAME, 'title').send_keys(new_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the article to be saved

        # Verify the new article is displayed
        self.assertIn(new_title, self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify forum is loaded
        self.assertIn("Community Forum", self.driver.page_source)

        # Post a new question
        new_post = "What are the best ways to reduce waste?"
        self.driver.find_element(By.NAME, 'post').send_keys(new_post)
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        time.sleep(1)  # Wait for the post to be saved

        # Verify the new post is displayed
        self.assertIn(new_post, self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Functionalities 8: Test navigation to other sections
        self.login("user1", "password1")

        # Navigate to Tips
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        time.sleep(1)
        self.assertIn("Sustainable Living Tips", self.driver.page_source)

        # Navigate to Articles
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        time.sleep(1)
        self.assertIn("Articles on Sustainable Living", self.driver.page_source)

        # Navigate to Forum
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)
        self.assertIn("Community Forum", self.driver.page_source)

    def test_data_storage_verification(self):
        # Functionalities 9: Test data storage verification
        new_username = "storage_user"
        new_password = "storage_pass"

        # Register a new user
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify user details are saved in users.txt
        with open('users.txt', 'r') as f:
            users = f.read()
            self.assertIn(f"{new_username}|{new_password}", users)

        # Login and submit a tip
        self.login(new_username, new_password)
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        time.sleep(1)
        new_tip = "Use rainwater harvesting"
        self.driver.find_element(By.NAME, 'tip').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Verify tip is saved in tips.txt
        with open('tips.txt', 'r') as f:
            tips = f.read()
            self.assertIn(new_tip, tips)

        # Submit an article
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        time.sleep(1)
        new_title = "Rainwater Harvesting"
        new_content = "Rainwater harvesting is a great way to conserve water."
        self.driver.find_element(By.NAME, 'title').send_keys(new_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Verify article is saved in articles.txt
        with open('articles.txt', 'r') as f:
            articles = f.read()
            self.assertIn(new_title, articles)

    def test_logout(self):
        # Functionalities 10: Test logging out
        self.login("user1", "password1")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
