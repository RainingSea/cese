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
        self.driver.get('http://localhost:8481/')  # Access the login page

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
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

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

        # Navigate to book management
        self.driver.find_element(By.LINK_TEXT, 'Book Management').click()
        time.sleep(1)  # Wait for the book management page to load

        # Add a new book
        self.driver.find_element(By.NAME, 'title').send_keys("New Book Title")
        self.driver.find_element(By.NAME, 'author').send_keys("New Author")
        self.driver.find_element(By.NAME, 'year').send_keys("2023")
        self.driver.find_element(By.XPATH, '//button[text()="Add Book"]').click()
        time.sleep(1)  # Wait for the confirmation message

        # Verify the confirmation message
        self.assertIn("Book added successfully.", self.driver.page_source)

    def test_search_books(self):
        # Functionalities 6: Search for a book
        self.login("admin", "admin123")

        # Navigate to search books
        self.driver.find_element(By.LINK_TEXT, 'Search Books').click()
        time.sleep(1)  # Wait for the search page to load

        # Search for a book
        self.driver.find_element(By.NAME, 'query').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results

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

        # Add a new book
        self.driver.find_element(By.LINK_TEXT, 'Book Management').click()
        time.sleep(1)  # Wait for the book management page to load

        self.driver.find_element(By.NAME, 'title').send_keys("Test Book")
        self.driver.find_element(By.NAME, 'author').send_keys("Test Author")
        self.driver.find_element(By.NAME, 'year').send_keys("2023")
        self.driver.find_element(By.XPATH, '//button[text()="Add Book"]').click()
        time.sleep(1)  # Wait for the confirmation message

        # Verify the book entry exists in the text file
        with open('books.txt', 'r') as file:
            contents = file.read()
            self.assertIn("Test Book|Test Author|2023", contents)

        # Delete the book
        self.driver.find_element(By.LINK_TEXT, 'Book Management').click()
        time.sleep(1)  # Wait for the book management page to load

        self.driver.find_element(By.XPATH, '//li[contains(text(), "Test Book")]/following-sibling::button[text()="Delete"]').click()
        time.sleep(1)  # Wait for the confirmation message

        # Verify the book entry is removed from the text file
        with open('books.txt', 'r') as file:
            contents = file.read()
            self.assertNotIn("Test Book|Test Author|2023", contents)

if __name__ == '__main__':
    unittest.main()
