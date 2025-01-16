import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestGreenLivingGuide(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'], cwd='D:/algorithm/agent/cese/dataset/SD-bench/codebase/website/GreenLivingGuide/code')
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8535/')

    def tearDown(self):
        # Close the web driver session and stop the web application
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

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Go to Registration').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Go to Registration').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.page_source)

    def test_view_sustainable_living_introduction(self):
        # Functionalities 4: Test viewing sustainable living introduction
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows introduction
        self.assertIn("Sustainable Living Tips", self.driver.page_source)

    def test_view_and_submit_sustainable_living_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("admin", "admin123")

        # Verify that tips are displayed
        self.assertIn("Reduce, reuse, recycle.", self.driver.page_source)

        # Submit a new tip
        new_tip = "Use solar panels."
        self.driver.find_element(By.NAME, 'content').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the tip to be submitted

        # Verify that the new tip is displayed
        self.assertIn(new_tip, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("admin", "admin123")

        # Verify that articles are displayed
        self.assertIn("The Importance of Sustainable Living", self.driver.page_source)

        # Submit a new article
        new_article_title = "Green Energy"
        new_article_content = "Green energy is the future."
        self.driver.find_element(By.NAME, 'title').send_keys(new_article_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_article_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the article to be submitted

        # Verify that the new article is displayed
        self.assertIn(new_article_title, self.driver.page_source)

    def test_participate_in_community_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "admin123")

        # Navigate to the forum
        self.driver.find_element(By.LINK_TEXT, 'Go to Forum').click()
        time.sleep(1)  # Wait for the forum page to load

        # Verify that the forum is loaded
        self.assertIn("Community Forum", self.driver.page_source)

        # Post a new question
        new_forum_post = "What are the best practices for sustainable living?"
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'content').send_keys(new_forum_post)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the post to be submitted

        # Verify that the new post is visible
        self.assertIn(new_forum_post, self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Functionalities 8: Test navigation to other sections
        self.login("admin", "admin123")

        # Navigate to the forum
        self.driver.find_element(By.LINK_TEXT, 'Go to Forum').click()
        time.sleep(1)  # Wait for the forum page to load

        # Verify that the forum is loaded
        self.assertIn("Community Forum", self.driver.page_source)

    def test_data_storage_verification(self):
        # Functionalities 9: Test data storage verification
        self.login("admin", "admin123")

        # Submit a new tip
        new_tip = "Use solar panels."
        self.driver.find_element(By.NAME, 'content').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the tip to be submitted

        # Verify the tip is saved in the tips.txt file
        with open('D:/algorithm/agent/cese/dataset/SD-bench/codebase/website/GreenLivingGuide/code/tips.txt', 'r') as file:
            tips = file.read()
            self.assertIn(new_tip, tips)

    def test_logout_functionality(self):
        # Functionalities 10: Test logout functionality
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
