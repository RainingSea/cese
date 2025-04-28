import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCultureFactsApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8313/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8313/register')
        
        # Verify Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8313/register')
        self.driver.find_element(By.NAME, 'username').send_keys("user1")
        self.driver.find_element(By.NAME, 'password').send_keys("test_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8313/')
        
        # Verify Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("user1", "user123")

        # Verify redirection to Dashboard
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8313/')
        self.login("user1", "wrong_password")

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_explore_cultures(self):
        # Functionality 3: Explore Cultures on the Dashboard Page
        self.login("user1", "user123")
        self.assertIn("Dashboard", self.driver.title)

        # Verify cultures are displayed
        cultures = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cultures), 0, "No cultures found.")

        # Click on a culture
        cultures[0].click()

        # Verify redirection to Culture Details Page
        self.assertIn("Culture Details", self.driver.title)

    def test_view_culture_details(self):
        # Functionality 4: View Culture Details
        self.login("user1", "user123")
        self.driver.get('http://localhost:8313/dashboard')
        cultures = self.driver.find_elements(By.TAG_NAME, 'li')
        cultures[0].click()

        # Verify culture details are displayed
        self.assertIn("Japanese", self.driver.page_source)
        self.assertIn("Known for its unique traditions", self.driver.page_source)

    def test_bookmark_culture_facts(self):
        # Functionality 6: Bookmark Culture Facts
        self.login("user1", "user123")
        self.driver.get('http://localhost:8313/culture/Japanese')

        # Click the "Bookmark" button (assuming it exists)
        self.driver.find_element(By.XPATH, '//button[text()="Bookmark"]').click()

        # Verify confirmation message
        self.assertIn("Bookmarked successfully", self.driver.page_source)

        # Navigate to Bookmarks Page
        self.driver.get('http://localhost:8313/bookmarks')

        # Verify bookmarked cultures are displayed
        self.assertIn("Japanese", self.driver.page_source)

    def test_view_and_manage_bookmarks(self):
        # Functionality 7: View and Manage Bookmarks
        self.login("user1", "user123")
        self.driver.get('http://localhost:8313/bookmarks')

        # Verify bookmarks are displayed
        bookmarks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(bookmarks), 0, "No bookmarks found.")

        # Click on the "Remove" button next to a bookmarked fact (assuming it exists)
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()

        # Verify confirmation message
        self.assertIn("Removed successfully", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
