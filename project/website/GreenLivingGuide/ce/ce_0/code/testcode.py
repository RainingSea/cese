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
        time.sleep(1)  # Wait for the server to start
        # Initialize the webdriver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8950/')

    def tearDown(self):
        # Close the web driver session and stop the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
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
        # Verify that the Dashboard Page shows the introduction
        self.assertIn("Dashboard", self.driver.title)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8950/tips')
        # Verify that tips are displayed
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips), 0, "No tips found.")

        # Submit a new tip
        new_tip_content = "Use energy-efficient appliances."
        self.driver.find_element(By.NAME, 'content').send_keys(new_tip_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be saved

        # Verify that the new tip is displayed
        self.assertIn(new_tip_content, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8950/articles')
        # Verify that articles are displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Submit a new article
        new_article_title = "New Sustainable Practice"
        new_article_content = "Details about the new practice."
        self.driver.find_element(By.NAME, 'title').send_keys(new_article_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_article_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()
        time.sleep(1)  # Wait for the article to be saved

        # Verify that the new article is displayed
        self.assertIn(new_article_title, self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8950/forum')
        # Verify that the forum is loaded
        forum_posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(forum_posts), 0, "No forum posts found.")

        # Post a new question
        new_forum_post = "What are the best ways to conserve water?"
        self.driver.find_element(By.NAME, 'content').send_keys(new_forum_post)
        self.driver.find_element(By.XPATH, '//button[text()="Post Question"]').click()
        time.sleep(1)  # Wait for the post to be saved

        # Verify that the new post is displayed
        self.assertIn(new_forum_post, self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Functionalities 8: Test navigation to other sections
        self.login("admin", "admin123")
        # Navigate to Articles
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        time.sleep(1)  # Wait for the page to load
        self.assertIn("Articles", self.driver.title)

        # Navigate to Tips
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        time.sleep(1)  # Wait for the page to load
        self.assertIn("Tips", self.driver.title)

        # Navigate to Forum
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the page to load
        self.assertIn("Community Forum", self.driver.title)

    def test_data_storage_verification(self):
        # Functionalities 9: Test data storage verification
        new_username = "storage_test_user"
        new_password = "storage_test_pass"

        # Register a new user
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the registration to complete

        # Verify user data is stored
        with open('users.txt', 'r') as file:
            users_data = file.read()
            self.assertIn(f"{new_username}|{new_password}", users_data)

        # Submit a new tip and verify storage
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8950/tips')
        new_tip_content = "Always turn off lights when not in use."
        self.driver.find_element(By.NAME, 'content').send_keys(new_tip_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be saved

        with open('tips.txt', 'r') as file:
            tips_data = file.read()
            self.assertIn(new_tip_content, tips_data)

        # Submit a new article and verify storage
        self.driver.get('http://localhost:8950/articles')
        new_article_title = "Eco-Friendly Transportation"
        new_article_content = "Using bicycles and public transport."
        self.driver.find_element(By.NAME, 'title').send_keys(new_article_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_article_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()
        time.sleep(1)  # Wait for the article to be saved

        with open('articles.txt', 'r') as file:
            articles_data = file.read()
            self.assertIn(f"{new_article_title}|{new_article_content}", articles_data)

    def test_logout(self):
        # Functionalities 10: Test logout functionality
        self.login("admin", "admin123")
        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load
        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
