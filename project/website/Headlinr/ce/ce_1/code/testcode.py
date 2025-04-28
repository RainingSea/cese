import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestHeadlinrApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8339/') 

    def tearDown(self):
        # Close the web driver session and terminate the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:8339/')  # Ensure we are on the login page
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_create_user_profile(self):
        # Functionalities 1: Create a new user profile
        self.login("admin", "admin123")  # Assuming admin is a valid user
        self.driver.get('http://localhost:8339/profile')  # Navigate to profile page

        # Create a new user profile
        self.driver.find_element(By.NAME, 'preferences').send_keys("sports,technology")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()

        # Verify that the profile is created successfully
        self.assertIn("Welcome to Headlinr", self.driver.page_source)

    def test_manage_user_preferences(self):
        # Functionalities 2: Update user preferences
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8339/profile')

        # Update preferences
        self.driver.find_element(By.NAME, 'preferences').clear()
        self.driver.find_element(By.NAME, 'preferences').send_keys("health,finance")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()

        # Verify that the preferences are updated
        self.assertIn("Welcome to Headlinr", self.driver.page_source)

    def test_generate_news_summaries(self):
        # Functionalities 3: Generate summaries for articles
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8339/news?query=technology')

        # Verify that summaries are generated and displayed
        self.assertIn("Breaking News: New Technology in AI", self.driver.page_source)

    def test_rank_news_articles(self):
        # Functionalities 4: Rank news articles
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8339/news?query=sports')

        # Verify that articles are ranked correctly
        self.assertIn("Sports Update: Local Team Wins Championship", self.driver.page_source)

    def test_bookmark_articles(self):
        # Functionalities 5: Bookmark an article
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8339/news?query=health')

        # Bookmark the first article
        self.driver.find_element(By.XPATH, '//li[contains(text(), "Health Tips: How to Stay Fit")]//button[text()="Bookmark"]').click()

        # Verify that the article is bookmarked
        self.assertIn("Article bookmarked successfully", self.driver.page_source)

    def test_share_articles(self):
        # Functionalities 6: Share a bookmarked article
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8339/news?query=technology')

        # Share the first article
        self.driver.find_element(By.XPATH, '//li[contains(text(), "Breaking News: New Technology in AI")]//button[text()="Share"]').click()

        # Verify that the article is shared successfully
        self.assertIn("Article shared successfully", self.driver.page_source)

    def test_user_interface_navigation(self):
        # Functionalities 7: Navigate to personalized news section
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8339/news')

        # Verify that personalized news content is displayed
        self.assertIn("News Articles", self.driver.page_source)

    def test_feedback_mechanism(self):
        # Functionalities 8: Submit user feedback
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8339/feedback')

        # Submit feedback
        self.driver.find_element(By.NAME, 'feedback').send_keys("Great application!")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify that feedback is submitted successfully
        self.assertIn("Thank you for your feedback", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
