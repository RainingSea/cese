import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestOnlineLibraryManagementSystem(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')  # Replace with the actual port from main.py

    def tearDown(self):
        # Close the web driver session and terminate the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Test user registration functionality
        self.driver.get('http://localhost:5000/register')  # Assuming there's a registration page
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.ID, 'username').send_keys(new_username)
        self.driver.find_element(By.ID, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_view_dashboard(self):
        # Test accessing the dashboard after login
        self.login("admin", "admin123")
        
        # Verify that the dashboard displays navigation options
        self.assertIn("Book Management", self.driver.page_source)
        self.assertIn("User Management", self.driver.page_source)
        self.assertIn("Search", self.driver.page_source)

    def test_manage_books(self):
        # Test adding a new book
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/book_management')  # Navigate to book management page

        # Add a new book
        self.driver.find_element(By.ID, 'title').send_keys("New Book Title")
        self.driver.find_element(By.ID, 'author').send_keys("New Author")
        self.driver.find_element(By.ID, 'isbn').send_keys("1234567890")
        self.driver.find_element(By.XPATH, '//input[@value="Add Book"]').click()
        time.sleep(1)  # Wait for the action to complete

        # Verify that the book was added (this assumes the book list updates on the page)
        self.assertIn("New Book Title", self.driver.page_source)

    def test_manage_user_accounts(self):
        # Test adding a new user
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/user_management')  # Navigate to user management page

        # Add a new user
        self.driver.find_element(By.ID, 'username').send_keys("new_user")
        self.driver.find_element(By.ID, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//input[@value="Add User"]').click()
        time.sleep(1)  # Wait for the action to complete

        # Verify that the user was added (this assumes the user list updates on the page)
        self.assertIn("new_user", self.driver.page_source)

    def test_search_books(self):
        # Test searching for a book
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/search')  # Navigate to search page

        # Search for a book
        self.driver.find_element(By.ID, 'query').send_keys("1984")
        self.driver.find_element(By.XPATH, '//input[@value="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        # Verify that the search results display the book's details
        self.assertIn("1984", self.driver.page_source)

    def test_user_logout(self):
        # Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_file_handling_for_data_storage(self):
        # Test adding a new book and checking the text file
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/book_management')

        # Add a new book
        self.driver.find_element(By.ID, 'title').send_keys("Test Book")
        self.driver.find_element(By.ID, 'author').send_keys("Test Author")
        self.driver.find_element(By.ID, 'isbn').send_keys("1111111111")
        self.driver.find_element(By.XPATH, '//input[@value="Add Book"]').click()
        time.sleep(1)

        # Check if the book entry exists in the books.txt file
        with open('books.txt', 'r') as file:
            content = file.read()
            self.assertIn("Test Book|Test Author|1111111111", content)

        # Delete the book and check if it is removed from the file
        self.driver.find_element(By.XPATH, '//button[text()="Delete Book"]').click()  # Assuming there's a delete button
        time.sleep(1)

        # Check if the book entry is removed from the books.txt file
        with open('books.txt', 'r') as file:
            content = file.read()
            self.assertNotIn("Test Book|Test Author|1111111111", content)

if __name__ == '__main__':
    unittest.main()
