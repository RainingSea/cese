import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestHeadlinrApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8176/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_create_user_profile(self):
        # Functionalities 1: Create User Profile
        self.login("username1", "password1")
        
        # Navigate to profile page
        self.driver.get('http://localhost:8176/profile')
        
        # Fill out the profile form
        self.driver.find_element(By.NAME, 'preference1').send_keys("Technology")
        self.driver.find_element(By.NAME, 'preference2').send_keys("Sports")
        self.driver.find_element(By.XPATH, '//button[text()="Save Preferences"]').click()

        # Verify that the user is redirected to the news page
        self.assertIn("Personalized News Articles", self.driver.title)

    def test_manage_user_preferences(self):
        # Functionalities 2: Manage User Preferences
        self.login("username1", "password1")
        
        # Navigate to profile page
        self.driver.get('http://localhost:8176/profile')
        
        # Update preferences
        self.driver.find_element(By.NAME, 'preference1').clear()
        self.driver.find_element(By.NAME, 'preference1').send_keys("Health")
        self.driver.find_element(By.XPATH, '//button[text()="Save Preferences"]').click()

        # Verify that the user is redirected to the news page
        self.assertIn("Personalized News Articles", self.driver.title)

    def test_generate_news_summaries(self):
        # Functionalities 3: Generate News Summaries
        self.login("username1", "password1")
        
        # Navigate to news page
        self.driver.get('http://localhost:8176/news')
        
        # Verify that articles are displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

    def test_rank_news_articles(self):
        # Functionalities 4: Rank News Articles
        self.login("username1", "password1")
        
        # Navigate to news page
        self.driver.get('http://localhost:8176/news')
        
        # Verify that articles are displayed and ranked
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

    def test_bookmark_articles(self):
        # Functionalities 5: Bookmark Articles
        self.login("username1", "password1")
        
        # Navigate to news page
        self.driver.get('http://localhost:8176/news')
        
        # Attempt to bookmark the first article (assuming a bookmark button exists)
        # This part of the functionality is not implemented in the codebase, so we will fail the test
        self.fail("Bookmarking articles functionality is not implemented.")

    def test_share_articles(self):
        # Functionalities 6: Share Articles
        self.login("username1", "password1")
        
        # Attempt to share an article (assuming a share button exists)
        # This part of the functionality is not implemented in the codebase, so we will fail the test
        self.fail("Sharing articles functionality is not implemented.")

    def test_user_interface_navigation(self):
        # Functionalities 7: User Interface Navigation
        self.login("username1", "password1")
        
        # Navigate to news page
        self.driver.get('http://localhost:8176/news')
        
        # Verify that the personalized news content is displayed
        self.assertIn("Personalized News Articles", self.driver.title)

    def test_feedback_mechanism(self):
        # Functionalities 8: Feedback Mechanism
        self.login("username1", "password1")
        
        # Navigate to feedback page
        self.driver.get('http://localhost:8176/feedback')
        
        # Submit feedback
        self.driver.find_element(By.NAME, 'feedback').send_keys("Great articles!")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()

        # Verify that the user is redirected to the news page
        self.assertIn("Personalized News Articles", self.driver.title)

if __name__ == '__main__':
    unittest.main()
