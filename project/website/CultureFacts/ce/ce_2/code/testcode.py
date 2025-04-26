import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCultureFactsApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the correct port

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:5000/login')  # Navigate to login page
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:5000/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:5000/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing user
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_user_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:5000/login')
        self.assertIn("Login", self.driver.title)

        # Successful login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Unsuccessful login
        self.driver.get('http://localhost:5000/login')
        self.login("admin", "wrongpassword")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_explore_cultures(self):
        # Functionality 3: Explore Cultures on the Dashboard Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/dashboard')
        self.assertIn("Culture Dashboard", self.driver.title)

        # Click on a culture
        self.driver.find_element(By.LINK_TEXT, "Japanese Culture").click()
        self.assertIn("Culture Details", self.driver.title)

    def test_view_culture_details(self):
        # Functionality 4: View Culture Details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/dashboard')
        self.driver.find_element(By.LINK_TEXT, "Japanese Culture").click()

        # Verify culture details are displayed
        self.assertIn("Japanese Culture", self.driver.page_source)

    def test_search_cultures(self):
        # Functionality 5: Search for Cultures or Facts
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/dashboard')

        # Search for a culture
        search_box = self.driver.find_element(By.NAME, 'search')
        search_box.send_keys("Japanese")
        search_box.submit()

        # Verify search results
        self.assertIn("Japanese Culture", self.driver.page_source)

        # Search for a non-existing culture
        search_box = self.driver.find_element(By.NAME, 'search')
        search_box.clear()
        search_box.send_keys("NonExistingCulture")
        search_box.submit()

        # Verify no results found message
        self.assertIn("No results found", self.driver.page_source)

    def test_bookmark_culture_facts(self):
        # Functionality 6: Bookmark Culture Facts
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/culture/Japanese Culture')
        self.driver.find_element(By.XPATH, '//button[text()="Bookmark"]').click()

        # Verify bookmark confirmation
        self.assertIn("Culture bookmarked", self.driver.page_source)

    def test_view_and_manage_bookmarks(self):
        # Functionality 7: View and Manage Bookmarks
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/bookmarks')

        # Verify bookmarks are displayed
        self.assertIn("Your Bookmarks", self.driver.page_source)

        # Remove a bookmark
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        self.assertIn("Bookmark removed", self.driver.page_source)

    def test_user_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

        # Attempt to access Dashboard after logout
        self.driver.get('http://localhost:5000/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # Functionality 9: Local Data Storage
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/add_culture')  # Assuming there's a page to add culture
        self.driver.find_element(By.NAME, 'culture_name').send_keys("New Culture")
        self.driver.find_element(By.XPATH, '//button[text()="Add Culture"]').click()

        # Refresh the Dashboard Page
        self.driver.get('http://localhost:5000/dashboard')
        self.assertIn("New Culture", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
