import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestGreenLivingGuideApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'], cwd='D:/Project/Datasets/SD-bench/codebase/website/GreenLivingGuide/code')
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8070')

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
        # Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Test navigation to the Registration Page
        self.driver.find_element(By.XPATH, '//form[@action="/register"]/button').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Login", self.driver.title)

    def test_user_registration(self):
        # Test user registration functionality
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.XPATH, '//form[@action="/register"]/input[@name="username"]').send_keys(new_username)
        self.driver.find_element(By.XPATH, '//form[@action="/register"]/input[@name="password"]').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//form[@action="/register"]/button').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_sustainable_living_introduction(self):
        # Test viewing sustainable living introduction after logging in
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows introduction
        self.assertIn("Dashboard", self.driver.title)

    def test_view_and_submit_sustainable_living_tips(self):
        # Test viewing and submitting sustainable living tips
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows tips
        tips = self.driver.find_elements(By.XPATH, '//h2[text()="Your Tips"]/following-sibling::ul/li')
        self.assertGreater(len(tips), 0, "No tips found.")

        # Submit a new tip
        new_tip = "Use reusable bags."
        self.driver.find_element(By.NAME, 'content').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be saved

        # Verify that the new tip is displayed
        self.assertIn(new_tip, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Test reading and submitting articles
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows articles
        articles = self.driver.find_elements(By.XPATH, '//h2[text()="Your Articles"]/following-sibling::ul/li')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Submit a new article
        new_article_title = "Green Energy"
        new_article_content = "Green energy is renewable and sustainable."
        self.driver.find_element(By.NAME, 'title').send_keys(new_article_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_article_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()
        time.sleep(1)  # Wait for the article to be saved

        # Verify that the new article is displayed
        self.assertIn(new_article_title, self.driver.page_source)

    def test_participate_in_community_forum(self):
        # Test participating in the community forum
        self.login("admin", "admin123")

        # Navigate to Forum
        self.driver.find_element(By.LINK_TEXT, 'Go to Forum').click()
        time.sleep(1)  # Wait for the forum page to load

        # Verify that the Forum Page has loaded
        self.assertIn("Community Forum", self.driver.title)

        # Post a new question
        new_post_content = "What are the best practices for sustainable living?"
        self.driver.find_element(By.NAME, 'content').send_keys(new_post_content)
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        time.sleep(1)  # Wait for the post to be saved

        # Verify that the new post is displayed
        self.assertIn(new_post_content, self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Test navigation to other sections
        self.login("admin", "admin123")

        # Navigate to Forum
        self.driver.find_element(By.LINK_TEXT, 'Go to Forum').click()
        time.sleep(1)  # Wait for the forum page to load

        # Verify that the Forum Page has loaded
        self.assertIn("Community Forum", self.driver.title)

    def test_data_storage_verification(self):
        # Test data storage verification
        self.login("admin", "admin123")

        # Submit a new tip
        new_tip = "Use reusable bags."
        self.driver.find_element(By.NAME, 'content').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be saved

        # Verify the new tip is saved in the tips storage file
        with open('D:/Project/Datasets/SD-bench/codebase/website/GreenLivingGuide/code/tips.txt', 'r') as file:
            tips = file.read()
            self.assertIn(new_tip, tips)

    def test_logout_functionality(self):
        # Test logging out
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
