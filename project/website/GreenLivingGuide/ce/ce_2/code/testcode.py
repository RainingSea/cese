import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestGreenLivingGuide(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8173/')  # Access the login page

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
        self.assertIn("Home", self.driver.title)  # Verify redirection to home page

    def test_view_and_submit_tips(self):
        # Functionalities 5: View and submit sustainable living tips
        self.login("admin", "admin123")
        
        # Verify existing tips are displayed
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips), 0, "No tips found.")

        # Submit a new tip
        self.driver.find_element(By.NAME, 'tip').send_keys("Reduce, Reuse, Recycle")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be submitted

        # Verify the new tip is displayed
        self.assertIn("Reduce, Reuse, Recycle", self.driver.page_source)

    def test_view_and_submit_articles(self):
        # Functionalities 6: Read and submit articles
        self.login("admin", "admin123")
        
        # Verify existing articles are displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Submit a new article
        self.driver.find_element(By.NAME, 'article').send_keys("The Importance of Biodiversity")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()
        time.sleep(1)  # Wait for the article to be submitted

        # Verify the new article is displayed
        self.assertIn("The Importance of Biodiversity", self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Participate in the community forum
        self.login("admin", "admin123")
        
        # Verify existing forum posts are displayed
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No forum posts found.")

        # Post a new question
        self.driver.find_element(By.NAME, 'post').send_keys("What are your favorite eco-friendly products?")
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        time.sleep(1)  # Wait for the post to be submitted

        # Verify the new post is displayed
        self.assertIn("What are your favorite eco-friendly products?", self.driver.page_source)

    def test_navigation(self):
        # Functionalities 8: Navigation to other sections
        self.login("admin", "admin123")

        # Navigate to tips section
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        time.sleep(1)  # Wait for the page to load
        self.assertIn("Sustainable Living Tips", self.driver.title)

        # Navigate to articles section
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        time.sleep(1)  # Wait for the page to load
        self.assertIn("Articles", self.driver.title)

        # Navigate to forum section
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the page to load
        self.assertIn("Community Forum", self.driver.title)

if __name__ == '__main__':
    unittest.main()
