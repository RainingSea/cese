import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestGreenLivingGuide(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8370/') 

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
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        # Assuming there is a "Register here" link on the login page
        self.fail("Not implemented")

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        # Assuming there is a registration page and functionality
        self.fail("Not implemented")

    def test_view_sustainable_living_intro(self):
        # Functionalities 4: Test viewing sustainable living introduction
        self.login("admin", "admin123")

        # Assuming there is an introduction section on the dashboard
        self.fail("Not implemented")

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Tips').click()
        time.sleep(1)  # Wait for the tips page to load

        # Verify existing tips are displayed
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips), 0, "No tips found.")

        # Submit a new tip
        self.driver.find_element(By.NAME, 'title').send_keys("New Tip")
        self.driver.find_element(By.NAME, 'content').send_keys("This is a new tip.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be saved

        # Verify the new tip is displayed
        self.assertIn("New Tip", self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Articles').click()
        time.sleep(1)  # Wait for the articles page to load

        # Verify existing articles are displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Submit a new article
        self.driver.find_element(By.NAME, 'title').send_keys("New Article")
        self.driver.find_element(By.NAME, 'content').send_keys("This is a new article.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()
        time.sleep(1)  # Wait for the article to be saved

        # Verify the new article is displayed
        self.assertIn("New Article", self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Community Forum').click()
        time.sleep(1)  # Wait for the forum page to load

        # Verify existing posts are displayed
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No forum posts found.")

        # Post a new question
        self.driver.find_element(By.NAME, 'content').send_keys("This is a new forum post.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Post"]').click()
        time.sleep(1)  # Wait for the post to be saved

        # Verify the new post is displayed
        self.assertIn("This is a new forum post.", self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Functionalities 8: Test navigation to other sections
        self.login("admin", "admin123")

        # Navigate to Tips
        self.driver.find_element(By.LINK_TEXT, 'View Tips').click()
        time.sleep(1)
        self.assertIn("Tips", self.driver.title)

        # Navigate to Articles
        self.driver.find_element(By.LINK_TEXT, 'View Articles').click()
        time.sleep(1)
        self.assertIn("Articles", self.driver.title)

        # Navigate to Forum
        self.driver.find_element(By.LINK_TEXT, 'Community Forum').click()
        time.sleep(1)
        self.assertIn("Community Forum", self.driver.title)

    def test_data_storage_verification(self):
        # Functionalities 9: Test data storage verification
        self.fail("Not implemented")

    def test_logout_functionality(self):
        # Functionalities 10: Test logout functionality
        self.login("admin", "admin123")

        # Assuming there is a logout button
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
