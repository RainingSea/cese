import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import os

class TestOnlineLibraryManagementSystem(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8204/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 2: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_view_dashboard(self):
        # Functionalities 3: Test accessing the dashboard after login
        self.login("admin", "admin123")
        
        # Verify that the dashboard displays navigation options
        self.assertIn("Manage Books", self.driver.page_source)
        self.assertIn("Manage Users", self.driver.page_source)
        self.assertIn("Search Books", self.driver.page_source)

    def test_manage_books(self):
        # Functionalities 4: Test adding a new book
        self.login("admin", "admin123")
        
        # Navigate to the book management page
        self.driver.get('http://localhost:8204/books')
        
        # Add a new book
        self.driver.find_element(By.NAME, 'title').send_keys("New Book Title")
        self.driver.find_element(By.NAME, 'author').send_keys("New Book Author")
        self.driver.find_element(By.XPATH, '//button[text()="Add Book"]').click()

        # Verify that the new book appears in the book list
        self.assertIn("New Book Title", self.driver.page_source)

    def test_search_books(self):
        # Functionalities 6: Test searching for a book
        self.login("admin", "admin123")
        
        # Navigate to the search page
        self.driver.get('http://localhost:8204/search')
        
        # Perform a search
        self.driver.find_element(By.NAME, 'query').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that the search results display the book's details
        self.assertIn("1984", self.driver.page_source)

    def test_user_logout(self):
        # Functionalities 7: Test logging out
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_file_handling_after_add_book(self):
        # Functionalities 8: Test file handling after adding a book
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8204/books')

        # Add a new book
        self.driver.find_element(By.NAME, 'title').send_keys("Test Book")
        self.driver.find_element(By.NAME, 'author').send_keys("Test Author")
        self.driver.find_element(By.XPATH, '//button[text()="Add Book"]').click()

        # Check if the book is added to the books.txt file
        with open('books.txt', 'r') as file:
            content = file.read()
            self.assertIn("Test Book|Test Author", content)

    def test_file_handling_after_delete_book(self):
        # Functionalities 8: Test file handling after deleting a book
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8204/books')

        # Add a book to delete
        self.driver.find_element(By.NAME, 'title').send_keys("Book to Delete")
        self.driver.find_element(By.NAME, 'author').send_keys("Author")
        self.driver.find_element(By.XPATH, '//button[text()="Add Book"]').click()

        # Delete the book
        # Assuming there's a delete button for each book in the list
        self.driver.find_element(By.XPATH, '//li[contains(text(), "Book to Delete")]/following-sibling::button[text()="Delete"]').click()

        # Check if the book is removed from the books.txt file
        with open('books.txt', 'r') as file:
            content = file.read()
            self.assertNotIn("Book to Delete|Author", content)

if __name__ == '__main__':
    unittest.main()
