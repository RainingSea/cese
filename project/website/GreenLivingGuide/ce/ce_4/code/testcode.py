import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time
import os

class TestGreenLivingGuide(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server a second to ensure it's up
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8954/')  # Open the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_login(self):
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

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_sustainable_living_intro(self):
        # Functionalities 4: Test viewing sustainable living introduction
        self.login("admin", "admin123")

        # Verify that the Home Page shows articles
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("admin", "admin123")

        # Navigate to Submit Tip Page
        self.driver.find_element(By.LINK_TEXT, 'Submit a Tip').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Tips Page shows tips
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips), 0, "No tips found.")

        # Submit a new tip
        new_tip = "Use solar panels for energy."
        self.driver.find_element(By.NAME, 'content').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//input[@value="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be saved

        # Verify that the new tip is displayed
        self.assertIn(new_tip, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("admin", "admin123")

        # Navigate to Articles Page
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Articles Page shows articles
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Test for submitting a new article is not implemented in the codebase
        self.fail("Submit article functionality not implemented")

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "admin123")

        # Navigate to Forum Page
        self.driver.find_element(By.LINK_TEXT, 'Community Forum').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Forum Page shows posts
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No forum posts found.")

        # Post a new question
        new_post = "What are the best practices for composting?"
        self.driver.find_element(By.NAME, 'content').send_keys(new_post)
        self.driver.find_element(By.XPATH, '//input[@value="Post"]').click()
        time.sleep(1)  # Wait for the post to be saved

        # Verify that the new post is displayed
        self.assertIn(new_post, self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Functionalities 8: Test navigation to other sections
        self.login("admin", "admin123")

        # Navigate to Articles Page
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Articles", self.driver.title)

        # Navigate to Tips Page
        self.driver.find_element(By.LINK_TEXT, 'Submit a Tip').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Submit Tip", self.driver.title)

        # Navigate to Forum Page
        self.driver.find_element(By.LINK_TEXT, 'Community Forum').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Community Forum", self.driver.title)

    def test_data_storage_verification(self):
        # Functionalities 9: Test data storage verification
        self.login("admin", "admin123")

        # Check users.txt for new user
        with open('users.txt', 'r') as file:
            users = file.read()
            self.assertIn("new_user|new_password", users)

        # Check tips.txt for new tip
        with open('tips.txt', 'r') as file:
            tips = file.read()
            self.assertIn("Use solar panels for energy.", tips)

        # Test for checking articles.txt for new article is not implemented in the codebase
        self.fail("Article storage verification not implemented")

    def test_logout(self):
        # Functionalities 10: Test logout functionality
        self.login("admin", "admin123")

        # Click the Logout button
        # Assuming there's a logout link/button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
