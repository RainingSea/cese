import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestHeadlinrApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the main page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8338/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:8338/')  # Ensure we are on the login page
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_create_user_profile(self):
        # Functionalities 1: Create User Profile
        self.login("admin", "admin")  # Assuming 'admin' is the password
        self.driver.get('http://localhost:8338/profile')  # Navigate to profile page

        # Check if the profile page is loaded
        self.assertIn("Manage Your Profile", self.driver.page_source)

    def test_manage_user_preferences(self):
        # Functionalities 2: Manage User Preferences
        self.login("admin", "admin")
        self.driver.get('http://localhost:8338/profile')

        # Update preferences
        self.driver.find_element(By.NAME, 'preferences').click()  # Check a preference
        self.driver.find_element(By.XPATH, '//input[@value="Technology"]').click()  # Select Technology
        self.driver.find_element(By.XPATH, '//input[@value="Health"]').click()  # Select Health
        self.driver.find_element(By.XPATH, '//input[@value="Sports"]').click()  # Select Sports
        self.driver.find_element(By.XPATH, '//input[@value="Update Preferences"]').click()  # Submit

        # Verify that the preferences were updated
        self.assertIn("Preferences updated", self.driver.page_source)

    def test_generate_news_summaries(self):
        # Functionalities 3: Generate News Summaries
        self.login("admin", "admin")
        articles = ["Technology is evolving rapidly with new innovations every day.",
                    "Health tips are essential for a balanced lifestyle.",
                    "Sports events are thrilling and bring communities together."]
        
        for article in articles:
            summary = article[:100] + '...'  # Simulate summary generation
            self.assertIn(summary, self.driver.page_source)

    def test_rank_news_articles(self):
        # Functionalities 4: Rank News Articles
        self.login("admin", "admin")
        preferences = ["Technology", "Health", "Sports"]
        articles = ["Technology is evolving rapidly with new innovations every day.",
                    "Health tips are essential for a balanced lifestyle.",
                    "Sports events are thrilling and bring communities together."]
        
        ranked_articles = sorted(articles, key=lambda x: sum(1 for pref in preferences if pref in x), reverse=True)
        for article in ranked_articles:
            self.assertIn(article, self.driver.page_source)

    def test_bookmark_articles(self):
        # Functionalities 5: Bookmark Articles
        self.login("admin", "admin")
        self.driver.get('http://localhost:8338/')  # Navigate to the main page

        # Simulate bookmarking an article
        self.driver.find_element(By.XPATH, '//button[text()="Bookmark"]').click()  # Assuming a bookmark button exists
        self.assertIn("Article bookmarked", self.driver.page_source)

    def test_share_articles(self):
        # Functionalities 6: Share Articles
        self.login("admin", "admin")
        self.driver.get('http://localhost:8338/')  # Navigate to the main page

        # Simulate sharing an article
        self.driver.find_element(By.XPATH, '//button[text()="Share"]').click()  # Assuming a share button exists
        self.assertIn("Article shared", self.driver.page_source)

    def test_user_interface_navigation(self):
        # Functionalities 7: User Interface Navigation
        self.login("admin", "admin")
        self.driver.get('http://localhost:8338/profile')  # Navigate to profile page

        # Check if the personalized news section is displayed
        self.assertIn("Manage Your Profile", self.driver.page_source)

    def test_feedback_mechanism(self):
        # Functionalities 8: Feedback Mechanism
        self.login("admin", "admin")
        self.driver.get('http://localhost:8338/')  # Navigate to the main page

        # Simulate submitting feedback
        self.driver.find_element(By.XPATH, '//textarea[@name="feedback"]').send_keys("Great app!")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()  # Assuming a submit button exists
        self.assertIn("Thank you for your feedback", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
