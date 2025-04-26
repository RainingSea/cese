import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCultureFactsApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8147/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8147/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8147/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already exists.", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid login
        self.assertIn("Dashboard", self.driver.title)

        # Attempt invalid login
        self.driver.get('http://localhost:8147/')
        self.login("admin", "wrongpassword")
        self.assertIn("Login", self.driver.title)  # Should remain on login page

    def test_explore_cultures(self):
        # Functionality 3: Explore Cultures on the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Culture Dashboard", self.driver.title)

        # Click on a culture
        culture_link = self.driver.find_element(By.LINK_TEXT, "Japanese")
        culture_link.click()
        self.assertIn("Culture Details", self.driver.title)

    def test_view_culture_details(self):
        # Functionality 4: View Culture Details
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Japanese").click()
        self.assertIn("Culture Details", self.driver.title)
        self.assertIn("A culture known for its unique traditions, art, and cuisine.", self.driver.page_source)

    def test_bookmark_culture(self):
        # Functionality 6: Bookmark Culture Facts
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Japanese").click()
        self.driver.find_element(By.XPATH, '//a[text()="Bookmark this culture"]').click()

        # Verify bookmark
        self.driver.get('http://localhost:8147/bookmarks')
        self.assertIn("Japanese", self.driver.page_source)

    def test_view_bookmarks(self):
        # Functionality 7: View and Manage Bookmarks
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Japanese").click()
        self.driver.find_element(By.XPATH, '//a[text()="Bookmark this culture"]').click()

        self.driver.get('http://localhost:8147/bookmarks')
        self.assertIn("Japanese", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
