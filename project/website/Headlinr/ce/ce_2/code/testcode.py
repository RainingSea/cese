import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestHeadlinrApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')  # Replace with the actual port from main.py

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
        self.login("admin", "admin123")  # Assuming admin credentials
        self.driver.get('http://localhost:5000/profile')  # Navigate to profile page

        # Fill out the profile creation form
        self.driver.find_element(By.NAME, 'name').send_keys("New User")
        self.driver.find_element(By.NAME, 'preferences').send_keys("news,sports")
        self.driver.find_element(By.XPATH, '//button[text()="Create Profile"]').click()

        # Verify profile creation success
        self.assertIn("Profile created successfully", self.driver.page_source)

    def test_manage_user_preferences(self):
        # Functionalities 2: Manage User Preferences
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/profile')  # Navigate to profile page

        # Update preferences
        self.driver.find_element(By.NAME, 'preferences').clear()
        self.driver.find_element(By.NAME, 'preferences').send_keys("technology,health")
        self.driver.find_element(By.XPATH, '//button[text()="Create Profile"]').click()

        # Verify preferences updated
        self.assertIn("Preferences updated successfully", self.driver.page_source)

    def test_generate_news_summaries(self):
        # Functionalities 3: Generate News Summaries
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/dashboard')  # Navigate to dashboard

        # Verify that summaries are generated
        self.assertIn("Personalized News Summaries", self.driver.page_source)

    def test_rank_news_articles(self):
        # Functionalities 4: Rank News Articles
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/dashboard')  # Navigate to dashboard

        # Check if articles are ranked (placeholder check)
        self.assertIn("Breaking News", self.driver.page_source)

    def test_bookmark_articles(self):
        # Functionalities 5: Bookmark Articles
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/dashboard')  # Navigate to dashboard

        # Bookmark an article
        self.driver.find_element(By.XPATH, '//button[text()="Bookmark"]').click()

        # Verify bookmark success
        self.assertIn("Article bookmarked successfully", self.driver.page_source)

    def test_share_articles(self):
        # Functionalities 6: Share Articles
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/dashboard')  # Navigate to dashboard

        # Share an article (placeholder action)
        self.driver.find_element(By.XPATH, '//button[text()="Share"]').click()

        # Verify share success
        self.assertIn("Article shared successfully", self.driver.page_source)

    def test_user_interface_navigation(self):
        # Functionalities 7: User Interface Navigation
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/dashboard')  # Navigate to dashboard

        # Verify personalized news content
        self.assertIn("Personalized News Summaries", self.driver.page_source)

    def test_feedback_mechanism(self):
        # Functionalities 8: Feedback Mechanism
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/feedback')  # Navigate to feedback page

        # Submit feedback
        self.driver.find_element(By.NAME, 'feedback').send_keys("Great summaries!")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify feedback submission success
        self.assertIn("Thank you for your feedback", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
