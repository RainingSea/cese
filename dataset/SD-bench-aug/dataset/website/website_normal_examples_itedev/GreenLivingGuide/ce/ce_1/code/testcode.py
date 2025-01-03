import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestGreenLivingGuide(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        # Close the web driver session and the application process
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
        self.login("admin", "admin123")  # Assuming these credentials exist
        self.assertIn("Dashboard", self.driver.title)

    def test_view_and_submit_tips(self):
        # Test viewing existing tips and submitting a new tip
        self.login("admin", "admin123")
        
        # Verify existing tips are displayed
        tips_list = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips_list), 0, "No tips found.")

        # Submit a new tip
        self.driver.find_element(By.NAME, 'tip_content').send_keys("New sustainable living tip.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be submitted

        # Verify the new tip is displayed
        self.assertIn("New sustainable living tip.", self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Test reading existing articles and submitting a new article
        self.login("admin", "admin123")
        
        # Verify existing articles are displayed
        articles_list = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles_list), 0, "No articles found.")

        # Submit a new article
        self.driver.find_element(By.NAME, 'article_title').send_keys("New Article Title")
        self.driver.find_element(By.NAME, 'article_content').send_keys("Content of the new article.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()
        time.sleep(1)  # Wait for the article to be submitted

        # Verify the new article is displayed
        self.assertIn("New Article Title", self.driver.page_source)

    def test_participate_in_forum(self):
        # Test accessing the forum and posting a new question
        self.login("admin", "admin123")
        
        # Access the forum
        self.driver.find_element(By.LINK_TEXT, 'Community Forum').click()
        time.sleep(1)  # Wait for the forum to load

        # Verify forum posts are displayed
        posts_list = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts_list), 0, "No forum posts found.")

        # Submit a new forum post
        self.driver.find_element(By.NAME, 'post_content').send_keys("This is a new forum post.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Post"]').click()
        time.sleep(1)  # Wait for the post to be submitted

        # Verify the new post is displayed
        self.assertIn("This is a new forum post.", self.driver.page_source)

    def test_logout_functionality(self):
        # Test logging out
        self.login("admin", "admin123")
        
        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the logout to complete

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
