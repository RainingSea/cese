import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestGreenLivingGuide(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8095/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and stop the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "pass123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        # This functionality is not implemented in the codebase
        self.fail("Navigate to Registration Page functionality not implemented")

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        # This functionality is not implemented in the codebase
        self.fail("User Registration functionality not implemented")

    def test_view_sustainable_living_introduction(self):
        # Functionalities 4: Test viewing sustainable living introduction
        # This functionality is not implemented in the codebase
        self.fail("View Sustainable Living Introduction functionality not implemented")

    def test_view_and_submit_sustainable_living_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("admin", "pass123")

        # Verify that the Dashboard Page shows tips
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips), 0, "No tips found.")

        # Submit a new tip
        new_tip_content = "Use solar panels"
        self.driver.find_element(By.NAME, 'content').send_keys(new_tip_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the page to reload

        # Verify that the new tip is displayed on the Dashboard
        self.assertIn(new_tip_content, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Go to Articles').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Articles Page shows articles
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Submit a new article
        new_article_title = "Eco-friendly Transportation"
        new_article_content = "Content about eco-friendly transportation."
        self.driver.find_element(By.NAME, 'title').send_keys(new_article_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_article_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the page to reload

        # Verify that the new article is displayed on the Articles Page
        self.assertIn(new_article_title, self.driver.page_source)

    def test_participate_in_community_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Go to Forum').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Forum Page shows posts
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No forum posts found.")

        # Post a new question
        new_forum_post = "How to start composting?"
        self.driver.find_element(By.NAME, 'content').send_keys(new_forum_post)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the page to reload

        # Verify that the new post is displayed on the Forum Page
        self.assertIn(new_forum_post, self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Functionalities 8: Test navigation to other sections
        self.login("admin", "pass123")

        # Navigate to Articles
        self.driver.find_element(By.LINK_TEXT, 'Go to Articles').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Articles", self.driver.title)

        # Navigate to Forum
        self.driver.find_element(By.LINK_TEXT, 'Go to Forum').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Community Forum", self.driver.title)

    def test_data_storage_verification(self):
        # Functionalities 9: Test data storage verification
        # This functionality requires file I/O checks which are not implemented here
        self.fail("Data Storage Verification functionality not implemented")

    def test_logout_functionality(self):
        # Functionalities 10: Test logout functionality
        # This functionality is not implemented in the codebase
        self.fail("Logout functionality not implemented")

if __name__ == '__main__':
    unittest.main()
