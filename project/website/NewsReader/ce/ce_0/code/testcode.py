import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestNewsReaderApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8354/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8354/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8354/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8354/')
        self.login("admin", "wrongpassword")  # Invalid password
        time.sleep(1)

        # Verify error message for incorrect credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_browse_news_categories(self):
        # Functionality 3: Browse News Categories on the Dashboard Page
        self.login("admin", "admin123")  # Valid login
        self.assertIn("Dashboard", self.driver.title)

        # Verify that articles are displayed
        articles = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(articles), 0, "No articles found on the dashboard.")

    def test_view_article_summaries(self):
        # Functionality 5: View Article Summaries in the News Feed
        self.login("admin", "admin123")  # Valid login
        self.assertIn("Dashboard", self.driver.title)

        # Click on the first article
        self.driver.find_element(By.XPATH, '//li[@class="list-group-item"]/a').click()
        time.sleep(1)

        # Verify that the Article Details Page is displayed
        self.assertIn("Article Details", self.driver.title)

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")  # Valid login

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the Dashboard Page after logging out
        self.driver.get('http://localhost:8354/dashboard')
        time.sleep(1)

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
