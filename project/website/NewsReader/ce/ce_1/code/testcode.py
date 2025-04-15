import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestNewsReaderApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8307/')

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

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.get('http://localhost:8307/register')
        
        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Register a new user
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify registration success (redirect to login page)
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8307/')
        
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Perform login with valid credentials
        self.login("admin", "admin123")

        # Verify redirection to Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Perform login with invalid credentials
        self.login("invalid_user", "invalid_pass")

        # Verify error message for invalid credentials
        self.assertIn("Login", self.driver.title)

    def test_browse_news_categories(self):
        # Login and navigate to Dashboard Page
        self.login("admin", "admin123")

        # Verify news categories are displayed
        categories = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(categories), 0, "No news categories found.")

        # Click on a specific news category (not implemented in codebase)
        self.fail("Browse news categories functionality not implemented")

    def test_search_for_topics(self):
        # Login and navigate to Dashboard Page
        self.login("admin", "admin123")

        # Verify search bar is visible
        search_bar = self.driver.find_element(By.NAME, 'query')
        self.assertIsNotNone(search_bar)

        # Search for a specific keyword
        search_bar.send_keys("Flask")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify search results are displayed
        self.assertIn("Flask Web Development", self.driver.page_source)

        # Search for a keyword with no related articles
        search_bar.clear()
        search_bar.send_keys("NonExistentKeyword")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify no articles found message
        self.assertIn("No articles found.", self.driver.page_source)

    def test_view_article_summaries(self):
        # Login and navigate to Dashboard Page
        self.login("admin", "admin123")

        # Verify article summaries are displayed
        articles = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Click on an article headline
        articles[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)

        # Verify redirection to Article Details Page
        self.assertIn("Article Details", self.driver.title)

    def test_user_logout(self):
        # Login and navigate to Dashboard Page
        self.login("admin", "admin123")

        # Perform logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to Dashboard Page
        self.driver.get('http://localhost:8307/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
