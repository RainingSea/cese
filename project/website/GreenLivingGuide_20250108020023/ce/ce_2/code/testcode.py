import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestGreenLivingGuide(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8307/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
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
        # This functionality is not implemented in the codebase
        self.fail("Navigation to Registration Page not implemented")

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        # This functionality is not implemented in the codebase
        self.fail("User Registration not implemented")

    def test_view_sustainable_living_intro(self):
        # Functionalities 4: Test viewing sustainable living introduction
        # This functionality is not implemented in the codebase
        self.fail("View Sustainable Living Introduction not implemented")

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Tips').click()
        time.sleep(1)

        # Verify that the Tips Page shows existing tips
        self.assertIn("Submit a Tip", self.driver.page_source)

        # Submit a new tip
        new_tip = "Use solar panels for energy."
        self.driver.find_element(By.NAME, 'content').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Verify that the new tip is saved
        with open('tips.txt', 'r') as f:
            tips = f.read()
            self.assertIn(new_tip, tips)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Articles').click()
        time.sleep(1)

        # Verify that the Articles Page shows existing articles
        self.assertIn("Submit an Article", self.driver.page_source)

        # Submit a new article
        new_article_title = "Green Energy Solutions"
        new_article_content = "Exploring the benefits of green energy."
        self.driver.find_element(By.NAME, 'title').send_keys(new_article_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_article_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Verify that the new article is saved
        with open('articles.txt', 'r') as f:
            articles = f.read()
            self.assertIn(new_article_title, articles)

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Community Forum').click()
        time.sleep(1)

        # Verify that the Forum Page is loaded
        self.assertIn("Community Forum", self.driver.page_source)

        # Post a new question
        new_post_content = "What are the best practices for composting?"
        self.driver.find_element(By.NAME, 'content').send_keys(new_post_content)
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        time.sleep(1)

        # Verify that the new post is saved
        with open('forum.txt', 'r') as f:
            forum_posts = f.read()
            self.assertIn(new_post_content, forum_posts)

    def test_navigation_to_other_sections(self):
        # Functionalities 8: Test navigation to other sections
        self.login("admin", "admin123")

        # Navigate to Tips
        self.driver.find_element(By.LINK_TEXT, 'Submit Tips').click()
        time.sleep(1)
        self.assertIn("Submit a Tip", self.driver.page_source)

        # Navigate to Articles
        self.driver.find_element(By.LINK_TEXT, 'Submit Articles').click()
        time.sleep(1)
        self.assertIn("Submit an Article", self.driver.page_source)

        # Navigate to Forum
        self.driver.find_element(By.LINK_TEXT, 'Community Forum').click()
        time.sleep(1)
        self.assertIn("Community Forum", self.driver.page_source)

    def test_data_storage_verification(self):
        # Functionalities 9: Test data storage verification
        # Check user data storage
        with open('users.txt', 'r') as f:
            users = f.read()
            self.assertIn("admin|admin123", users)

        # Check tips data storage
        with open('tips.txt', 'r') as f:
            tips = f.read()
            self.assertIn("Reduce, reuse, recycle.", tips)

        # Check articles data storage
        with open('articles.txt', 'r') as f:
            articles = f.read()
            self.assertIn("The Benefits of Sustainable Living", articles)

    def test_logout(self):
        # Functionalities 10: Test logout functionality
        # This functionality is not implemented in the codebase
        self.fail("Logout Functionality not implemented")

if __name__ == '__main__':
    unittest.main()
