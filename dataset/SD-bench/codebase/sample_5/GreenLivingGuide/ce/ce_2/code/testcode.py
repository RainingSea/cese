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

        # Initialize the webdriver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8456/')

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
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

        # Verify that the Home Page has loaded
        self.assertIn("Welcome to Sustainable Living", self.driver.page_source)

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

    def test_view_sustainable_living_intro(self):
        # Functionalities 4: Test viewing sustainable living introduction
        self.login("admin", "admin123")

        # Verify that the Home Page shows the introduction
        self.assertIn("Welcome to Sustainable Living", self.driver.page_source)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that tips are displayed
        self.assertIn("Sustainable Living Tips", self.driver.page_source)

        # Submit a new tip
        new_tip = "Use solar panels"
        self.driver.find_element(By.NAME, 'tip').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be saved

        # Verify that the new tip is displayed
        self.assertIn(new_tip, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that articles are displayed
        self.assertIn("Articles on Sustainable Living", self.driver.page_source)

        # Submit a new article
        new_article_title = "Green Energy"
        new_article_content = "Green energy is the future."
        self.driver.find_element(By.NAME, 'title').send_keys(new_article_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_article_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()
        time.sleep(1)  # Wait for the article to be saved

        # Verify that the new article is displayed
        self.assertIn(new_article_title, self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the forum is loaded
        self.assertIn("Community Forum", self.driver.page_source)

        # Post a new question
        new_post = "What are the best practices for recycling?"
        self.driver.find_element(By.NAME, 'message').send_keys(new_post)
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        time.sleep(1)  # Wait for the post to be saved

        # Verify that the new post is displayed
        self.assertIn(new_post, self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Functionalities 8: Test navigation to other sections
        self.login("admin", "admin123")

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
        self.login("admin", "admin123")

        # Check users.txt for user data
        with open('users.txt', 'r') as file:
            users_data = file.read()
        self.assertIn("admin|admin123", users_data)

        # Submit a new tip and check tips.txt
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        time.sleep(1)
        new_tip = "Use LED bulbs"
        self.driver.find_element(By.NAME, 'tip').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)
        with open('tips.txt', 'r') as file:
            tips_data = file.read()
        self.assertIn(new_tip, tips_data)

        # Submit a new article and check articles.txt
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        time.sleep(1)
        new_article_title = "Eco-Friendly Transport"
        new_article_content = "Bicycles are eco-friendly."
        self.driver.find_element(By.NAME, 'title').send_keys(new_article_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_article_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()
        time.sleep(1)
        with open('articles.txt', 'r') as file:
            articles_data = file.read()
        self.assertIn(new_article_title, articles_data)

    def test_logout(self):
        # Functionalities 10: Test logging out
        self.login("admin", "admin123")

        # Click the Logout button (assuming there's a logout button)
        # Since the logout functionality is not implemented in the provided code, this test will fail
        self.fail("Logout functionality not implemented")

if __name__ == '__main__':
    unittest.main()
