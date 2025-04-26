import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestOnlineLibraryManagementSystem(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8203/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 2: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_view_dashboard(self):
        # Functionalities 3: Test accessing the dashboard after login
        self.login("admin", "admin123")

        # Verify that the dashboard displays book management options
        self.assertIn("Welcome to the Library Dashboard", self.driver.page_source)

    def test_add_book(self):
        # Functionalities 4: Test adding a new book
        self.login("admin", "admin123")

        # Add a new book
        self.driver.find_element(By.NAME, 'title').send_keys("New Book Title")
        self.driver.find_element(By.NAME, 'author').send_keys("New Author")
        self.driver.find_element(By.XPATH, '//input[@value="Add Book"]').click()
        time.sleep(1)  # Wait for the book to be added

        # Verify that the new book appears in the dashboard
        self.assertIn("New Book Title", self.driver.page_source)

    def test_user_logout(self):
        # Functionalities 7: Test logging out
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_file_handling_after_add_book(self):
        # Functionalities 8: Check if the book is added to the file
        self.login("admin", "admin123")

        # Add a new book
        book_title = "File Check Book"
        self.driver.find_element(By.NAME, 'title').send_keys(book_title)
        self.driver.find_element(By.NAME, 'author').send_keys("File Check Author")
        self.driver.find_element(By.XPATH, '//input[@value="Add Book"]').click()
        time.sleep(1)  # Wait for the book to be added

        # Verify that the book entry exists in the books.txt file
        with open('books.txt', 'r') as file:
            books = file.read()
            self.assertIn(book_title, books)

    def test_file_handling_after_delete_book(self):
        # Functionalities 8: Check if the book is deleted from the file
        self.login("admin", "admin123")

        # Add a book to delete later
        book_title = "Delete Check Book"
        self.driver.find_element(By.NAME, 'title').send_keys(book_title)
        self.driver.find_element(By.NAME, 'author').send_keys("Delete Check Author")
        self.driver.find_element(By.XPATH, '//input[@value="Add Book"]').click()
        time.sleep(1)  # Wait for the book to be added

        # Delete the book
        self.driver.find_element(By.LINK_TEXT, f'Delete').click()
        time.sleep(1)  # Wait for the book to be deleted

        # Verify that the book entry is removed from the books.txt file
        with open('books.txt', 'r') as file:
            books = file.read()
            self.assertNotIn(book_title, books)

if __name__ == '__main__':
    unittest.main()
