import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestHeadlinrApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8633/')  # Access the home page

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def test_create_user_profile(self):
        # Functionalities 1: Create User Profile
        self.driver.get('http://localhost:8633/profile')
        self.driver.find_element(By.ID, 'username').send_keys('new_user')
        self.driver.find_element(By.ID, 'preferences').send_keys('sports,technology')
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()

        # Verify redirection to the home page
        self.assertIn("Headlinr - News Summaries", self.driver.title)

    def test_manage_user_preferences(self):
        # Functionalities 2: Manage User Preferences
        self.driver.get('http://localhost:8633/profile')
        self.driver.find_element(By.ID, 'username').send_keys('admin')
        self.driver.find_element(By.ID, 'preferences').send_keys('technology,health')
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()

        # Verify redirection to the home page
        self.assertIn("Headlinr - News Summaries", self.driver.title)

    def test_generate_news_summaries(self):
        # Functionalities 3: Generate News Summaries
        self.driver.get('http://localhost:8633/')
        summaries = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(summaries), 0, "No news summaries found.")

    def test_rank_news_articles(self):
        # Functionalities 4: Rank News Articles
        self.fail("Not implemented")

    def test_bookmark_articles(self):
        # Functionalities 5: Bookmark Articles
        self.driver.get('http://localhost:8633/bookmarks')
        bookmarks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(bookmarks), 0, "No bookmarks found.")

    def test_share_articles(self):
        # Functionalities 6: Share Articles
        self.fail("Not implemented")

    def test_user_interface_navigation(self):
        # Functionalities 7: User Interface Navigation
        self.driver.get('http://localhost:8633/')
        self.assertIn("Headlinr - News Summaries", self.driver.title)

    def test_feedback_mechanism(self):
        # Functionalities 8: Feedback Mechanism
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
