import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestNewsReaderApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8656/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and stop the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        # Verify registration page is displayed
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.ID, 'username').send_keys(new_username)
        self.driver.find_element(By.ID, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the login page to load

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'username').send_keys("admin")
        self.driver.find_element(By.ID, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("already taken", self.driver.page_source)

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "admin123")

        # Verify redirection to dashboard
        self.assertIn("Dashboard", self.driver.title)

        # Test invalid login
        self.driver.get('http://localhost:8656/')  # Navigate back to login page
        self.login("invalid_user", "wrong_password")

        # Verify error message for invalid credentials
        self.assertIn("incorrect", self.driver.page_source)

    def test_browse_news_categories(self):
        # Test browsing news categories
        self.login("admin", "admin123")

        # Verify news categories are displayed
        categories = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(categories), 0, "No news categories found.")

        # Click on a news category
        categories[0].click()
        time.sleep(1)

        # Verify articles related to the category are displayed
        self.assertIn("Full text of", self.driver.page_source)

    def test_search_for_specific_topics(self):
        # Test searching for specific topics
        self.login("admin", "admin123")

        # Verify search bar is visible
        self.assertIn("Search", self.driver.page_source)

        # Search for a keyword
        self.driver.find_element(By.NAME, 'search').send_keys("Tech")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify articles related to the keyword are displayed
        self.assertIn("Tech Update", self.driver.page_source)

        # Search for a non-existing keyword
        self.driver.find_element(By.NAME, 'search').clear()
        self.driver.find_element(By.NAME, 'search').send_keys("NonExistingKeyword")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify no articles found message
        self.assertIn("No articles found", self.driver.page_source)

    def test_view_article_summaries(self):
        # Test viewing article summaries
        self.login("admin", "admin123")

        # Verify articles with summaries are displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Click on an article headline
        articles[0].click()
        time.sleep(1)

        # Verify full text of the article is displayed
        self.assertIn("Full text of", self.driver.page_source)

    def test_user_logout(self):
        # Test user logout functionality
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the dashboard
        self.driver.get('http://localhost:8656/dashboard')
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
