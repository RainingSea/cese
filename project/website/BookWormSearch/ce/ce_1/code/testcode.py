import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestBookWormSearch(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start

        # Initialize the webdriver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8588/')

    def tearDown(self):
        # Close the web driver session and stop the Flask app
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
        time.sleep(1)

        # Verify Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter valid username and password
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("Register", self.driver.title)  # Assuming it stays on the same page

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("admin", "admin123")

        # Verify redirection to Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8588/')
        self.login("invalid_user", "wrong_password")

        # Verify error message for invalid login
        self.assertIn("Login", self.driver.title)  # Assuming it stays on the same page

    def test_book_search(self):
        # Login and navigate to Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Test search functionality (not implemented in the codebase)
        self.fail("Book search functionality not implemented")

    def test_view_book_details(self):
        # Login and navigate to Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Click on a book to view details
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)

        # Verify Book Details Page
        self.assertIn("The Great Gatsby", self.driver.title)
        self.assertIn("F. Scott Fitzgerald", self.driver.page_source)
        self.assertIn("A story about the American dream.", self.driver.page_source)

    def test_add_book_to_reading_list(self):
        # Test adding book to reading list (not implemented in the codebase)
        self.fail("Add book to reading list functionality not implemented")

    def test_view_and_manage_reading_list(self):
        # Login and navigate to Reading List Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'My Reading List').click()
        time.sleep(1)

        # Verify Reading List Page
        self.assertIn("My Reading List", self.driver.title)
        self.assertIn("The Great Gatsby", self.driver.page_source)

        # Test removing book from reading list (not implemented in the codebase)
        self.fail("Manage reading list functionality not implemented")

    def test_user_logout(self):
        # Login and navigate to Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Test logout functionality (not implemented in the codebase)
        self.fail("User logout functionality not implemented")

    def test_local_data_storage(self):
        # Test local data storage functionality (not implemented in the codebase)
        self.fail("Local data storage functionality not implemented")

if __name__ == '__main__':
    unittest.main()
