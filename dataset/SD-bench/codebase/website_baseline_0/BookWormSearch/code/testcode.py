import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestBookWormSearch(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'], cwd='D:\\algorithm\\agent\\cese\\dataset\\SD-bench\\codebase\\website\\BookWormSearch\\code')
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8525/')

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
        # Functionality 1: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the registration page to load

        # Verify registration page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the registration process

        # Verify registration success
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for duplicate username
        self.assertIn("Username already exists", self.driver.page_source)

    def test_user_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify successful login
        self.assertIn("Dashboard", self.driver.title)

        # Test invalid login
        self.driver.get('http://localhost:8525/')
        self.login("invalid_user", "wrong_password")

        # Verify login failure
        self.assertIn("Login", self.driver.title)

    def test_book_search(self):
        # Functionality 3: Book Search
        self.login("admin", "admin123")

        # Verify dashboard page
        self.assertIn("Dashboard", self.driver.title)

        # Search for a book
        self.driver.find_element(By.NAME, 'search').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify search results
        self.assertIn("1984", self.driver.page_source)

        # Search for a non-existent book
        self.driver.find_element(By.NAME, 'search').clear()
        self.driver.find_element(By.NAME, 'search').send_keys("NonExistentBook")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify no results found
        self.assertIn("No results found", self.driver.page_source)

    def test_view_book_details(self):
        # Functionality 4: View Book Details
        self.login("admin", "admin123")

        # Click on a book to view details
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)

        # Verify book details page
        self.assertIn("1984", self.driver.page_source)
        self.assertIn("George Orwell", self.driver.page_source)

    def test_add_book_to_reading_list(self):
        # Functionality 5: Add Book to Reading List
        self.login("admin", "admin123")

        # Add a book to the reading list
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()
        time.sleep(1)

        # Verify book added to reading list
        self.assertIn("Added 1984 to your reading list", self.driver.page_source)

    def test_view_and_manage_reading_list(self):
        # Functionality 6: View and Manage Reading List
        self.login("admin", "admin123")

        # Navigate to reading list
        self.driver.find_element(By.LINK_TEXT, 'Reading List').click()
        time.sleep(1)

        # Verify reading list page
        self.assertIn("Your Reading List", self.driver.page_source)

        # Remove a book from the reading list
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        time.sleep(1)

        # Verify book removed from reading list
        self.assertNotIn("1984", self.driver.page_source)

    def test_user_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")

        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify logout success
        self.assertIn("Login", self.driver.title)

        # Attempt to access dashboard after logout
        self.driver.get('http://localhost:8525/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # Functionality 8: Local Data Storage
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
