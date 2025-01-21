import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time
import os

class TestGreenLivingGuide(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8953/')

    def tearDown(self):
        # Close the web driver session and terminate the server process
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
        # Assuming there's a link to registration which is not implemented in the codebase
        self.fail("Registration page navigation not implemented")

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        # Assuming registration functionality is not implemented in the codebase
        self.fail("User registration functionality not implemented")

    def test_view_sustainable_living_introduction(self):
        # Functionalities 4: Test viewing sustainable living introduction
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows introduction
        self.assertIn("Dashboard", self.driver.title)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8953/tips')

        # Verify existing tips are displayed
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips), 0, "No tips found.")

        # Submit a new tip
        new_tip_content = "Use solar panels to save energy."
        self.driver.find_element(By.NAME, 'tip_content').send_keys(new_tip_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be saved

        # Verify the new tip is displayed
        self.assertIn(new_tip_content, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8953/articles')

        # Verify existing articles are displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Submit a new article
        new_article_title = "Benefits of Planting Trees"
        new_article_content = "Planting trees helps reduce carbon footprint."
        self.driver.find_element(By.NAME, 'title').send_keys(new_article_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_article_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()
        time.sleep(1)  # Wait for the article to be saved

        # Verify the new article is displayed
        self.assertIn(new_article_title, self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8953/forum')

        # Verify forum posts are displayed
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No forum posts found.")

        # Post a new question
        new_post_content = "What are the best ways to conserve water?"
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'content').send_keys(new_post_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Post"]').click()
        time.sleep(1)  # Wait for the post to be saved

        # Verify the new post is displayed
        self.assertIn(new_post_content, self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Functionalities 8: Test navigation to other sections
        self.login("admin", "admin123")

        # Navigate to Articles
        self.driver.get('http://localhost:8953/articles')
        self.assertIn("Articles", self.driver.title)

        # Navigate to Tips
        self.driver.get('http://localhost:8953/tips')
        self.assertIn("Sustainable Living Tips", self.driver.title)

        # Navigate to Forum
        self.driver.get('http://localhost:8953/forum')
        self.assertIn("Community Forum", self.driver.title)

    def test_data_storage_verification(self):
        # Functionalities 9: Test data storage verification
        # Check users.txt for user details
        with open('users.txt', 'r') as file:
            users_data = file.read()
            self.assertIn("admin|admin123", users_data)

        # Check tips.txt for new tip
        with open('tips.txt', 'r') as file:
            tips_data = file.read()
            self.assertIn("Use solar panels to save energy.", tips_data)

        # Check articles.txt for new article
        with open('articles.txt', 'r') as file:
            articles_data = file.read()
            self.assertIn("Benefits of Planting Trees|Planting trees helps reduce carbon footprint.", articles_data)

    def test_logout_functionality(self):
        # Functionalities 10: Test logout functionality
        # Assuming logout functionality is not implemented in the codebase
        self.fail("Logout functionality not implemented")

if __name__ == '__main__':
    unittest.main()
