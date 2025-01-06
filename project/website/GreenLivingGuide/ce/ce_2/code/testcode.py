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
        self.driver.get('http://localhost:8172/')  # Open the login page

    def tearDown(self):
        # Close the web driver session
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
        self.login("user1", "password1")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
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

    def test_view_sustainable_living_introduction(self):
        # Functionalities 4: Test viewing sustainable living introduction
        self.login("user1", "password1")

        # Verify that the Dashboard Page shows the introduction
        self.assertIn("Welcome to the Dashboard", self.driver.page_source)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Tips Page has loaded
        self.assertIn("Sustainable Living Tips", self.driver.page_source)

        # Submit a new tip
        tip_content = "Use reusable bags instead of plastic."
        self.driver.find_element(By.NAME, 'tip').send_keys(tip_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be saved

        # Verify that the new tip is displayed
        self.assertIn(tip_content, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Articles Page has loaded
        self.assertIn("Articles on Sustainable Living", self.driver.page_source)

        # Submit a new article
        article_title = "New Sustainable Practice"
        article_content = "This is a new article about sustainable practices."
        self.driver.find_element(By.NAME, 'title').send_keys(article_title)
        self.driver.find_element(By.NAME, 'content').send_keys(article_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()
        time.sleep(1)  # Wait for the article to be saved

        # Verify that the new article is displayed
        self.assertIn(article_title, self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Forum Page has loaded
        self.assertIn("Community Forum", self.driver.page_source)

        # Post a new question
        forum_content = "What are the best practices for sustainable living?"
        self.driver.find_element(By.NAME, 'content').send_keys(forum_content)
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        time.sleep(1)  # Wait for the post to be saved

        # Verify that the new post is displayed
        self.assertIn(forum_content, self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Functionalities 8: Test navigation to other sections
        self.login("user1", "password1")

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
        self.fail("Not implemented")

    def test_logout_functionality(self):
        # Functionalities 10: Test logout functionality
        self.login("user1", "password1")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
