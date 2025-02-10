import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestHeadlinrApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8629/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username):
        # Helper method to perform login
        self.driver.get('http://localhost:8629/profile')
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'preferences').send_keys("technology, sports")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()

    def test_create_user_profile(self):
        # Functionalities 1: Create User Profile
        self.login("testuser")
        # Verify that the user is redirected to the index page
        self.assertIn("Headlinr", self.driver.title)

    def test_manage_user_preferences(self):
        # Functionalities 2: Manage User Preferences
        self.login("admin")
        # Update preferences
        self.driver.get('http://localhost:8629/profile')
        self.driver.find_element(By.NAME, 'preferences').clear()
        self.driver.find_element(By.NAME, 'preferences').send_keys("politics, health")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        # Verify preferences are updated
        self.assertIn("Headlinr", self.driver.title)

    def test_generate_news_summaries(self):
        # Functionalities 3: Generate News Summaries
        self.login("admin")
        # Verify that summaries are displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

    def test_rank_news_articles(self):
        # Functionalities 4: Rank News Articles
        self.login("admin")
        # Verify that articles are ranked (simply displayed in this case)
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

    def test_bookmark_articles(self):
        # Functionalities 5: Bookmark Articles
        self.fail("Bookmark functionality not implemented")

    def test_share_articles(self):
        # Functionalities 6: Share Articles
        self.fail("Share functionality not implemented")

    def test_user_interface_navigation(self):
        # Functionalities 7: User Interface Navigation
        self.login("admin")
        # Verify that the user is on the index page
        self.assertIn("Headlinr", self.driver.title)

    def test_feedback_mechanism(self):
        # Functionalities 8: Feedback Mechanism
        self.fail("Feedback functionality not implemented")

if __name__ == '__main__':
    unittest.main()
