import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestBookWormSearch(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8993/') 

    def tearDown(self):
        # Close the web driver session and stop the application
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
        self.assertIn("Register", self.driver.title)

        # Register a new user
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Check for error message (not implemented in codebase)
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8993/')
        self.login("invalid_user", "wrong_password")
        self.assertIn("Login", self.driver.title)

    def test_book_search(self):
        # Login and navigate to the Dashboard
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Search for a valid book
        self.driver.find_element(By.NAME, 'search').send_keys('1984')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)
        self.assertIn("1984", self.driver.page_source)

        # Search for a non-existent book
        self.driver.find_element(By.NAME, 'search').clear()
        self.driver.find_element(By.NAME, 'search').send_keys('NonExistentBook')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)
        self.assertNotIn("NonExistentBook", self.driver.page_source)

    def test_view_book_details(self):
        # Login and navigate to the Dashboard
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Click on a book to view details
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        self.assertIn("The Great Gatsby", self.driver.title)
        self.assertIn("F. Scott Fitzgerald", self.driver.page_source)
        self.assertIn("A novel about the American dream.", self.driver.page_source)

    def test_add_book_to_reading_list(self):
        # Navigate to Book Details and add to Reading List
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        self.driver.find_element(By.LINK_TEXT, 'Add to Reading List').click()
        time.sleep(1)

        # Verify the book is added to the Reading List
        self.driver.find_element(By.LINK_TEXT, 'My Reading List').click()
        self.assertIn("The Great Gatsby", self.driver.page_source)

    def test_view_and_manage_reading_list(self):
        # Login and navigate to the Reading List
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'My Reading List').click()
        self.assertIn("Reading List", self.driver.title)

        # Remove a book from the Reading List (not implemented in codebase)
        self.fail("Remove book functionality not implemented")

    def test_user_logout(self):
        # Login and then logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access Dashboard after logout
        self.driver.get('http://localhost:8993/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # Add a book to the reading list and verify persistence
        self.fail("Data persistence functionality not implemented")

if __name__ == '__main__':
    unittest.main()
