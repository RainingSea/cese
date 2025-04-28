import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestOnlineLibraryManagementSystem(unittest.TestCase):

    def setUp(self):
        # Start the main application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the correct port

    def tearDown(self):
        # Close the web driver session and terminate the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Functionalities 1: User Registration
        self.driver.get('http://localhost:5000/user_management')  # Navigate to User Management
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register User"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the user management page
        self.assertIn("User Management", self.driver.title)

    def test_user_login(self):
        # Functionalities 2: User Login
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_view_dashboard(self):
        # Functionalities 3: View Dashboard
        self.login("admin", "admin123")
        
        # Verify that the dashboard displays navigation options
        self.assertIn("Manage Books", self.driver.page_source)
        self.assertIn("Manage Users", self.driver.page_source)

    def test_manage_books(self):
        # Functionalities 4: Manage Books
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/book_management')  # Navigate to Book Management

        book_title = "New Book Title"
        book_author = "New Book Author"

        # Input book details for adding a new book
        self.driver.find_element(By.NAME, 'title').send_keys(book_title)
        self.driver.find_element(By.NAME, 'author').send_keys(book_author)
        self.driver.find_element(By.XPATH, '//button[text()="Add Book"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the book is added
        self.assertIn(book_title, self.driver.page_source)

    def test_manage_user_accounts(self):
        # Functionalities 5: Manage User Accounts
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/user_management')  # Navigate to User Management

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register User"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is added
        self.assertIn(new_username, self.driver.page_source)

    def test_search_books(self):
        # Functionalities 6: Search Books
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/book_management')  # Navigate to Book Management

        search_query = "1984"  # Assuming this book exists
        self.driver.find_element(By.NAME, 'search').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results

        # Verify the search results display the book's details
        self.assertIn("1984", self.driver.page_source)

    def test_user_logout(self):
        # Functionalities 7: User Logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_file_handling_for_data_storage(self):
        # Functionalities 8: File Handling for Data Storage
        self.login("admin", "admin123")

        # Add a new book
        self.driver.get('http://localhost:5000/book_management')  # Navigate to Book Management
        book_title = "Test Book"
        book_author = "Test Author"

        self.driver.find_element(By.NAME, 'title').send_keys(book_title)
        self.driver.find_element(By.NAME, 'author').send_keys(book_author)
        self.driver.find_element(By.XPATH, '//button[text()="Add Book"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check if the book entry exists in the books.txt file
        with open('books.txt', 'r') as file:
            books = file.readlines()
            self.assertIn(f"{book_title}|{book_author}\n", books)

        # Delete the book
        self.driver.find_element(By.XPATH, f'//li[contains(text(), "{book_title}")]/following-sibling::button[text()="Delete"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check if the book entry is removed from the books.txt file
        with open('books.txt', 'r') as file:
            books = file.readlines()
            self.assertNotIn(f"{book_title}|{book_author}\n", books)

if __name__ == '__main__':
    unittest.main()
