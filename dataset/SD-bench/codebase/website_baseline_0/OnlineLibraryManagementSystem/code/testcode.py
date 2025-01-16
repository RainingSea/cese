import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os
import json

class TestOnlineLibraryManagementSystem(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8543/')

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
        # Functionalities 1: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register User"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Functionalities 2: Test user login functionality
        self.login("test_user", "test_password")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_view_dashboard(self):
        # Functionalities 3: Test viewing the dashboard
        self.login("test_user", "test_password")

        # Verify that the Dashboard Page shows navigation options
        self.assertIn("Manage Books", self.driver.page_source)

    def test_manage_books(self):
        # Functionalities 4: Test adding a new book
        self.login("test_user", "test_password")
        self.driver.find_element(By.LINK_TEXT, 'Go to Book Management').click()
        time.sleep(1)  # Wait for the next page to load

        book_title = "New Book"
        book_author = "Author Name"

        # Fill out the new book form
        self.driver.find_element(By.NAME, 'title').send_keys(book_title)
        self.driver.find_element(By.NAME, 'author').send_keys(book_author)
        self.driver.find_element(By.XPATH, '//button[text()="Add Book"]').click()
        time.sleep(1)  # Wait for the book to be added

        # Verify that the new book is displayed in the list
        self.assertIn(book_title, self.driver.page_source)

    def test_manage_user_accounts(self):
        # Functionalities 5: Not implemented in the codebase
        self.fail("Not implemented")

    def test_search_books(self):
        # Functionalities 6: Test searching for a book
        self.login("test_user", "test_password")
        self.driver.find_element(By.LINK_TEXT, 'Go to Book Management').click()
        time.sleep(1)  # Wait for the next page to load

        search_query = "New Book"
        self.driver.find_element(By.NAME, 'query').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results

        # Verify that the search results display the book's details
        self.assertIn(search_query, self.driver.page_source)

    def test_user_logout(self):
        # Functionalities 7: Test logging out
        self.login("test_user", "test_password")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_file_handling_for_data_storage(self):
        # Functionalities 8: Test file handling for data storage
        self.login("test_user", "test_password")
        self.driver.find_element(By.LINK_TEXT, 'Go to Book Management').click()
        time.sleep(1)  # Wait for the next page to load

        book_title = "File Handling Book"
        book_author = "File Author"

        # Add a new book
        self.driver.find_element(By.NAME, 'title').send_keys(book_title)
        self.driver.find_element(By.NAME, 'author').send_keys(book_author)
        self.driver.find_element(By.XPATH, '//button[text()="Add Book"]').click()
        time.sleep(1)  # Wait for the book to be added

        # Verify that the book entry exists in the text file
        with open('books.txt', 'r') as file:
            books = json.load(file)
            self.assertTrue(any(book['title'] == book_title for book in books))

        # Delete the book
        self.driver.find_element(By.NAME, 'title').send_keys(book_title)
        self.driver.find_element(By.XPATH, '//button[text()="Delete Book"]').click()
        time.sleep(1)  # Wait for the book to be deleted

        # Verify that the book entry is removed from the text file
        with open('books.txt', 'r') as file:
            books = json.load(file)
            self.assertFalse(any(book['title'] == book_title for book in books))

if __name__ == '__main__':
    unittest.main()
