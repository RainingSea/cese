import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineLibraryManagementSystem(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8202/')  # Access the login page

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

    def test_user_registration(self):
        # Functionalities 1: Register a new user
        self.driver.get('http://localhost:8202/user_management')  # Navigate to user management
        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register User"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the user management page
        self.assertIn("User Management", self.driver.title)

    def test_user_login(self):
        # Functionalities 2: Log in with valid credentials
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_view_dashboard(self):
        # Functionalities 3: Access the dashboard after logging in
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8202/dashboard')  # Access the dashboard

        # Verify that the dashboard displays navigation options
        self.assertIn("Manage Books", self.driver.page_source)
        self.assertIn("Manage Users", self.driver.page_source)

    def test_manage_books(self):
        # Functionalities 4: Add a new book
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8202/book_management')  # Navigate to book management

        book_title = "New Book Title"
        book_author = "New Book Author"

        # Input book details
        self.driver.find_element(By.NAME, 'title').send_keys(book_title)
        self.driver.find_element(By.NAME, 'author').send_keys(book_author)
        self.driver.find_element(By.XPATH, '//button[text()="Add Book"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the book is successfully added
        self.assertIn(book_title, self.driver.page_source)

    def test_manage_user_accounts(self):
        # Functionalities 5: Add a new user and view the list of users
        self.test_user_registration()  # Register a new user
        self.driver.get('http://localhost:8202/user_management')  # Navigate to user management

        # Verify that the newly added user appears in the user list
        self.assertIn("test_user", self.driver.page_source)

    def test_search_books(self):
        # Functionalities 6: Search for a book
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8202/book_management')  # Navigate to book management

        # Search for a book (this functionality is not implemented in the codebase)
        self.fail("Search books functionality not implemented")

    def test_user_logout(self):
        # Functionalities 7: Log out of the account
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_file_handling_for_data_storage(self):
        # Functionalities 8: Check file handling after adding and deleting a book
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8202/book_management')  # Navigate to book management

        book_title = "File Handling Book"
        book_author = "File Handling Author"

        # Add a new book
        self.driver.find_element(By.NAME, 'title').send_keys(book_title)
        self.driver.find_element(By.NAME, 'author').send_keys(book_author)
        self.driver.find_element(By.XPATH, '//button[text()="Add Book"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the book entry exists in the text file
        with open('books.txt', 'r') as file:
            books = file.read()
            self.assertIn(book_title, books)

        # Delete the book (this functionality is not implemented in the codebase)
        self.fail("Delete book functionality not implemented")

if __name__ == '__main__':
    unittest.main()
