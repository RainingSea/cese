import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestCultureFactsApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8312/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
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
        self.driver.get('http://localhost:8312/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8312/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8312/')
        self.login("invalid_user", "invalid_password")
        time.sleep(1)

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_explore_cultures(self):
        # Functionality 3: Explore Cultures on the Dashboard Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8312/dashboard')

        # Verify that culture facts are displayed
        culture_facts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(culture_facts), 0, "No culture facts found.")

        # Click on a culture to view details
        culture_facts[0].click()
        time.sleep(1)

        # Verify that the Culture Details Page has loaded
        self.assertIn("Culture Details", self.driver.title)

    def test_view_culture_details(self):
        # Functionality 4: View Culture Details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8312/dashboard')
        culture_facts = self.driver.find_elements(By.TAG_NAME, 'li')
        culture_facts[0].click()
        time.sleep(1)

        # Verify that culture details are displayed
        self.assertIn("Culture Details", self.driver.title)
        self.assertIn("Japanese culture", self.driver.page_source)

    def test_bookmark_culture(self):
        # Functionality 6: Bookmark Culture Facts
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8312/dashboard')
        culture_facts = self.driver.find_elements(By.TAG_NAME, 'li')
        culture_facts[0].click()
        time.sleep(1)

        # Click the bookmark button
        self.driver.find_element(By.XPATH, '//button[text()="Bookmark"]').click()
        time.sleep(1)

        # Verify that the culture has been bookmarked
        self.driver.get('http://localhost:8312/bookmarks?username=admin')
        self.assertIn("Japanese culture", self.driver.page_source)

    def test_view_bookmarks(self):
        # Functionality 7: View and Manage Bookmarks
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8312/bookmarks?username=admin')

        # Verify that bookmarks are displayed
        self.assertIn("Your Bookmarks", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
