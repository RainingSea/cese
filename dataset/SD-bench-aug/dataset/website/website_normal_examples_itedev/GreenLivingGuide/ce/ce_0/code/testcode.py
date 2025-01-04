import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestGreenLivingGuideApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        # Close the web driver and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:5000')  # Ensure we are on the login page
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "admin123")  # Use valid credentials
        self.assertIn("Dashboard", self.driver.title)

    def test_view_and_submit_tips(self):
        # Test viewing and submitting sustainable living tips
        self.login("admin", "admin123")
        
        # Verify existing tips are displayed
        tips_list = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips_list), 0, "No tips found.")

        # Submit a new tip
        self.driver.find_element(By.LINK_TEXT, 'View Tips').click()
        time.sleep(1)  # Wait for the tips page to load
        self.driver.find_element(By.NAME, 'tip_content').send_keys("Test Tip: Reduce water usage.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be submitted

        # Verify the new tip is displayed
        self.assertIn("Test Tip: Reduce water usage.", self.driver.page_source)

    def test_view_and_submit_articles(self):
        # Test viewing and submitting articles
        self.login("admin", "admin123")

        # Verify existing articles are displayed
        self.driver.find_element(By.LINK_TEXT, 'View Articles').click()
        time.sleep(1)  # Wait for the articles page to load
        articles_list = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles_list), 0, "No articles found.")

        # Submit a new article
        self.driver.find_element(By.NAME, 'article_title').send_keys("Test Article Title")
        self.driver.find_element(By.NAME, 'article_content').send_keys("This is a test article content.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()
        time.sleep(1)  # Wait for the article to be submitted

        # Verify the new article is displayed
        self.assertIn("Test Article Title", self.driver.page_source)

    def test_participate_in_forum(self):
        # Test accessing and posting in the community forum
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Community Forum').click()
        time.sleep(1)  # Wait for the forum page to load

        # Verify existing forum posts are displayed
        posts_list = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts_list), 0, "No forum posts found.")

        # Submit a new forum post
        self.driver.find_element(By.NAME, 'post_content').send_keys("This is a test forum post.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Post"]').click()
        time.sleep(1)  # Wait for the post to be submitted

        # Verify the new post is displayed
        self.assertIn("This is a test forum post.", self.driver.page_source)

    def test_logout_functionality(self):
        # Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the logout to complete

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
