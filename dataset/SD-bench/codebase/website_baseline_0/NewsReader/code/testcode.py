import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestNewsReaderApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8540/')

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
        # Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("username is already taken", self.driver.page_source)

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Test invalid login
        self.driver.get('http://localhost:8540/login')
        self.login("invalid_user", "invalid_pass")

        # Verify error message for invalid credentials
        self.assertIn("credentials are incorrect", self.driver.page_source)

    def test_browse_news_categories(self):
        # Test browsing news categories on the Dashboard Page
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows articles
        articles = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Click on a specific news category
        self.driver.find_element(By.LINK_TEXT, 'Sports Highlights').click()
        time.sleep(1)

        # Verify the user is shown articles related to the selected category
        self.assertIn("Sports Highlights", self.driver.page_source)

    def test_search_for_specific_topics(self):
        # Test searching for specific topics or keywords
        self.login("admin", "admin123")

        # Verify the search bar is visible
        search_bar = self.driver.find_element(By.NAME, 'query')
        self.assertIsNotNone(search_bar)

        # Search for a specific keyword
        search_bar.send_keys("Technology")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify articles related to the keyword are displayed
        self.assertIn("Technology Update", self.driver.page_source)

        # Search for a keyword with no related articles
        search_bar.clear()
        search_bar.send_keys("NonExistentKeyword")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify message indicating no articles found
        self.assertIn("no articles were found", self.driver.page_source)

    def test_view_article_summaries(self):
        # Test viewing article summaries in the news feed
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows articles with headlines, summaries, and sources
        articles = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Click on an article headline
        self.driver.find_element(By.LINK_TEXT, 'Breaking News').click()
        time.sleep(1)

        # Verify the user is redirected to the Article Details Page
        self.assertIn("Article Details", self.driver.title)

    def test_user_logout(self):
        # Test user logout functionality
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the Dashboard Page
        self.driver.get('http://localhost:8540/dashboard')
        time.sleep(1)

        # Verify access to the Dashboard is denied
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
