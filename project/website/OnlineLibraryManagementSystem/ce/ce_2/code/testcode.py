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
        self.driver.get('http://localhost:8482/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
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
        self.driver.get('http://localhost:8482/user_management')  # Navigate to user management
        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Add User"]').click()
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
        
        # Verify that the dashboard displays navigation options
        self.assertIn("Book Management", self.driver.page_source)
        self.assertIn("User Management", self.driver.page_source)
        self.assertIn("Search Books", self.driver.page_source)

    def test_manage_books(self):
        # Functionalities 4: Add a new book
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8482/book_management')  # Navigate to book management

        book_title = "New Book Title"
        book_author = "New Book Author"
        book_year = "2023"

        # Input book details
        self.driver.find_element(By.NAME, 'title').send_keys(book_title)
        self.driver.find_element(By.NAME, 'author').send_keys(book_author)
        self.driver.find_element(By.NAME, 'year').send_keys(book_year)
        self.driver.find_element(By.XPATH, '//button[text()="Add Book"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the book addition confirmation message
        self.assertIn("Book added successfully.", self.driver.page_source)

    def test_search_books(self):
        # Functionalities 6: Search for a book
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8482/search_books')  # Navigate to search books

        search_query = "1984"
        self.driver.find_element(By.NAME, 'query').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the search results display the book's details
        self.assertIn("1984", self.driver.page_source)

    def test_user_logout(self):
        # Functionalities 7: Log out of the account
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_file_handling(self):
        # Functionalities 8: Check file handling for data storage
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8482/book_management')  # Navigate to book management

        book_title = "File Handling Book"
        book_author = "File Author"
        book_year = "2023"

        # Input book details
        self.driver.find_element(By.NAME, 'title').send_keys(book_title)
        self.driver.find_element(By.NAME, 'author').send_keys(book_author)
        self.driver.find_element(By.NAME, 'year').send_keys(book_year)
        self.driver.find_element(By.XPATH, '//button[text()="Add Book"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the book addition confirmation message
        self.assertIn("Book added successfully.", self.driver.page_source)

        # Check if the book is in the books.txt file
        with open('books.txt', 'r') as file:
            content = file.read()
            self.assertIn(f"{book_title}|{book_author}|{book_year}", content)

        # Delete the book for cleanup
        self.driver.find_element(By.XPATH, f'//li[contains(text(), "{book_title}")]//following-sibling::button[text()="Delete"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the book deletion
        self.assertNotIn(book_title, content)

if __name__ == '__main__':
    unittest.main()
