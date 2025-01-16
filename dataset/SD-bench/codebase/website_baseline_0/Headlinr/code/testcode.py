import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestHeadlinrApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8536')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.XPATH, '//input[@value="Create Profile"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_create_user_profile(self):
        # Functionalities 1: Create User Profile
        self.login("new_user")
        # Verify that the profile is created and redirected to the index page
        self.assertIn("News Summary App", self.driver.title)

    def test_manage_user_preferences(self):
        # Functionalities 2: Manage User Preferences
        self.driver.get('http://localhost:8536/profile')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'preferences').send_keys("science, technology")
        self.driver.find_element(By.XPATH, '//input[@value="Update Profile"]').click()
        time.sleep(1)  # Wait for the update to complete
        # Verify that the preferences are updated (no direct confirmation message in UI)
        self.assertIn("News Summary App", self.driver.title)

    def test_generate_news_summaries(self):
        # Functionalities 3: Generate News Summaries
        self.login("admin")
        self.driver.find_element(By.LINK_TEXT, 'View Articles').click()
        time.sleep(1)  # Wait for the articles page to load
        # Verify that summaries are displayed
        summaries = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(summaries), 0, "No article summaries found.")

    def test_rank_news_articles(self):
        # Functionalities 4: Rank News Articles
        self.fail("Not implemented")

    def test_bookmark_articles(self):
        # Functionalities 5: Bookmark Articles
        self.fail("Not implemented")

    def test_share_articles(self):
        # Functionalities 6: Share Articles
        self.fail("Not implemented")

    def test_user_interface_navigation(self):
        # Functionalities 7: User Interface Navigation
        self.login("admin")
        self.driver.find_element(By.LINK_TEXT, 'View Articles').click()
        time.sleep(1)  # Wait for the articles page to load
        # Verify that the personalized news content is displayed
        self.assertIn("Articles", self.driver.title)

    def test_feedback_mechanism(self):
        # Functionalities 8: Feedback Mechanism
        self.driver.get('http://localhost:8536')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'comments').send_keys("Great app!")
        self.driver.find_element(By.XPATH, '//input[@value="Submit Feedback"]').click()
        time.sleep(1)  # Wait for the feedback submission
        # Verify that feedback is submitted (no direct confirmation message in UI)
        self.assertIn("News Summary App", self.driver.title)

if __name__ == '__main__':
    unittest.main()
