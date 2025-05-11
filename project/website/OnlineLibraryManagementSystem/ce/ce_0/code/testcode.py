import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestOnlineLibraryManagementSystem(unittest.TestCase):

    def setUp(self):
        # Start the main application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8480/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the application process
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
        self.driver.get('http://localhost:8480/users')  # Navigate to user management
        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register User"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user registration confirmation message
        self.assertIn("User registered successfully.", self.driver.page_source)

    def test_user_login(self):
        # Functionalities 2: Log in with valid credentials
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_view_dashboard(self):
        # Functionalities 3: Access the dashboard after logging in
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8480/dashboard')  # Navigate to dashboard

        # Verify that the dashboard displays navigation options
        self.assertIn("Manage Books", self.driver.page_source)
        self.assertIn("Manage Users", self.driver.page_source)

    def test_manage_books(self):
        # Functionalities 4: Add a new book
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8480/books')  # Navigate to book management

        book_title = "New Book Title"
        book_author = "New Book Author"

        # Input book details
        self.driver.find_element(By.NAME, 'title').send_keys(book_title)
        self.driver.find_element(By.NAME, 'author').send_keys(book_author)
        self.driver.find_element(By.XPATH, '//button[text()="Add Book"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the book addition confirmation message
        self.assertIn("Book added successfully.", self.driver.page_source)

    def test_manage_user_accounts(self):
        # Functionalities 5: Add a new user and view the user list
        self.test_user_registration()  # Register a new user
        self.driver.get('http://localhost:8480/users')  # Navigate to user management

        # Verify the newly added user appears in the user list
        self.assertIn("test_user", self.driver.page_source)

    def test_search_books(self):
        # Functionalities 6: Search for a book
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8480/books')  # Navigate to book management

        # Search for a book that exists
        self.driver.find_element(By.NAME, 'query').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        # Verify the search results display the book's details
        self.assertIn("1984", self.driver.page_source)

    def test_user_logout(self):
        # Functionalities 7: Log out of the account
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)
        self.assertIn("You have been logged out.", self.driver.page_source)

    def test_file_handling(self):
        # Functionalities 8: Check file handling for data storage
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8480/books')  # Navigate to book management

        book_title = "File Handling Book"
        book_author = "File Author"

        # Add a new book
        self.driver.find_element(By.NAME, 'title').send_keys(book_title)
        self.driver.find_element(By.NAME, 'author').send_keys(book_author)
        self.driver.find_element(By.XPATH, '//button[text()="Add Book"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the book entry exists in the text file
        with open('books.txt', 'r') as file:
            content = file.read()
            self.assertIn(book_title, content)

        # Delete the book
        self.driver.find_element(By.XPATH, f'//li[contains(text(), "{book_title}")]//following-sibling::button[text()="Delete"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the book entry is removed from the text file
        with open('books.txt', 'r') as file:
            content = file.read()
            self.assertNotIn(book_title, content)

if __name__ == '__main__':
    unittest.main()
