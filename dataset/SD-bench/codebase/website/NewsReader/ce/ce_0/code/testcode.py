import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestNewsReaderApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8652/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and stop the server
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
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the page to load

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the page to load
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the page to load

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)  # Assuming the page reloads on error

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8652/')  # Navigate back to login
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)  # Assuming the page reloads on error

    def test_browse_news_categories(self):
        # Login successfully
        self.login("admin", "admin123")

        # Verify a list of news categories is displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Click on a specific news category (e.g., first article)
        articles[0].click()
        time.sleep(1)  # Wait for the page to load

        # Verify the user is shown a list of articles related to the selected category
        self.assertIn("Source:", self.driver.page_source)

    def test_search_for_specific_topics(self):
        # This functionality is not implemented in the codebase
        self.fail("Search functionality not implemented")

    def test_view_article_summaries(self):
        # Login successfully
        self.login("admin", "admin123")

        # Verify a list of articles with headlines, summaries, and sources is displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Click on an article headline
        articles[0].click()
        time.sleep(1)  # Wait for the page to load

        # Verify the user is redirected to the Article Details Page
        self.assertIn("Source:", self.driver.page_source)

    def test_user_logout(self):
        # Login successfully
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the page to load

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the Dashboard Page
        self.driver.get('http://localhost:8652/dashboard')
        time.sleep(1)  # Wait for the page to load

        # Verify access to the Dashboard is denied
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
