import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestNewsReaderApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8309/')  # Navigate to the login page

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
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)  # Still on the registration page

    def test_user_login(self):
        # Verify that the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8309/')  # Navigate back to the login page
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)  # Still on the login page

    def test_browse_news_categories(self):
        # Login successfully
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows categories
        categories = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(categories), 0, "No categories found.")

    def test_search_for_specific_topics(self):
        # Login successfully
        self.login("admin", "admin123")

        # Verify that the search bar is visible
        search_bar = self.driver.find_element(By.NAME, 'query')
        self.assertIsNotNone(search_bar)

        # Enter a specific keyword and submit
        search_bar.send_keys("Tech")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that articles related to the keyword are displayed
        self.assertIn("Search Results", self.driver.title)

        # Enter a keyword that has no related articles
        self.driver.get('http://localhost:8309/dashboard')  # Navigate back to the dashboard
        search_bar = self.driver.find_element(By.NAME, 'query')
        search_bar.send_keys("NonExistentKeyword")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that a message is displayed indicating no articles were found
        self.assertIn("No articles found", self.driver.page_source)

    def test_view_article_summaries(self):
        # Login successfully
        self.login("admin", "admin123")

        # Verify that a list of articles is displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Click on an article headline
        articles[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Article Details Page is displayed
        self.assertIn("Article Details", self.driver.title)

    def test_user_logout(self):
        # Login successfully
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the Dashboard Page
        self.driver.get('http://localhost:8309/dashboard')
        time.sleep(1)  # Wait for the next page to load

        # Verify that access to the Dashboard is denied
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
