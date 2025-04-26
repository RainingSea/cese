import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import os

class TestGreenLivingGuideApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8171/')  # Use the port from main.py

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration_page(self):
        # Functionalities 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Create Account').click()
        self.assertIn("Create Account", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Create Account').click()
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Create Account"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_sustainable_living_intro(self):
        # Functionalities 4: View Sustainable Living Introduction
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_view_and_submit_tips(self):
        # Functionalities 5: View and Submit Sustainable Living Tips
        self.login("admin", "admin123")

        # Verify existing tips are displayed
        tips = self.driver.find_elements(By.CLASS_NAME, 'tip-item')
        self.assertGreater(len(tips), 0, "No tips found.")

        # Submit a new tip
        new_tip = "Use reusable bags."
        self.driver.find_element(By.NAME, 'tip').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()

        # Verify the new tip is displayed
        self.assertIn(new_tip, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Read and Submit Articles
        self.login("admin", "admin123")

        # Verify existing articles are displayed
        articles = self.driver.find_elements(By.CLASS_NAME, 'article-item')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Submit a new article
        new_article = "The Benefits of Solar Energy."
        self.driver.find_element(By.NAME, 'article').send_keys(new_article)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()

        # Verify the new article is displayed
        self.assertIn(new_article, self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Participate in the Community Forum
        self.login("admin", "admin123")

        # Verify forum is loaded
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.assertIn("Forum", self.driver.title)

        # Post a new question
        new_post = "What are your favorite eco-friendly products?"
        self.driver.find_element(By.NAME, 'post').send_keys(new_post)
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()

        # Verify the new post is visible
        self.assertIn(new_post, self.driver.page_source)

    def test_logout_functionality(self):
        # Functionalities 10: Logout Functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
