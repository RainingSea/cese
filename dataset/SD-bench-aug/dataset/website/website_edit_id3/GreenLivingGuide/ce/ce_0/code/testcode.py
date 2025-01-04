import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestGreenLivingGuide(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'], cwd='D:/Project/CE/CE/project/website/GreenLivingGuide/ce/ce_0/code')
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8131')

    def tearDown(self):
        # Close the web driver session and terminate the web application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "adminpass")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
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
        self.login("admin", "adminpass")

        # Verify that the Dashboard Page shows the introduction
        self.assertIn("Sustainable Living", self.driver.page_source)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("admin", "adminpass")

        # Verify that the Dashboard Page shows tips
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips), 0, "No tips found.")

        # Submit a new tip
        new_tip = "Use solar panels"
        self.driver.find_element(By.NAME, 'content').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the tip to be saved

        # Verify that the new tip is displayed
        self.assertIn(new_tip, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("admin", "adminpass")

        # Verify that the Dashboard Page shows articles
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Submit a new article
        new_article_title = "Eco-Friendly Homes"
        new_article_content = "Building homes with sustainable materials."
        self.driver.find_element(By.NAME, 'title').send_keys(new_article_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_article_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the article to be saved

        # Verify that the new article is displayed
        self.assertIn(new_article_title, self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "adminpass")

        # Navigate to the Forum Page
        self.driver.find_element(By.LINK_TEXT, 'Go to Forum').click()
        time.sleep(1)  # Wait for the forum page to load

        # Verify that the Forum Page shows posts
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No forum posts found.")

        # Post a new question
        new_post_content = "How to start composting?"
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'content').send_keys(new_post_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the post to be saved

        # Verify that the new post is displayed
        self.assertIn(new_post_content, self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Functionalities 8: Test navigation to other sections
        self.login("admin", "adminpass")

        # Navigate to the Forum Page
        self.driver.find_element(By.LINK_TEXT, 'Go to Forum').click()
        time.sleep(1)  # Wait for the forum page to load

        # Verify that the Forum Page has loaded
        self.assertIn("Community Forum", self.driver.title)

    def test_data_storage_verification(self):
        # Functionalities 9: Test data storage verification
        self.login("admin", "adminpass")

        # Check users.txt for the new user
        with open('users.txt', 'r') as file:
            users_content = file.read()
            self.assertIn("new_user|new_password|", users_content)

        # Check tips.txt for the new tip
        with open('tips.txt', 'r') as file:
            tips_content = file.read()
            self.assertIn("Use solar panels", tips_content)

        # Check articles.txt for the new article
        with open('articles.txt', 'r') as file:
            articles_content = file.read()
            self.assertIn("Eco-Friendly Homes|Building homes with sustainable materials.", articles_content)

    def test_logout_functionality(self):
        # Functionalities 10: Test logout functionality
        self.login("admin", "adminpass")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
