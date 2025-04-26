import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import os

class TestVirtualBookPublishingApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8284/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigation to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_access_dashboard(self):
        # Functionalities 4: Accessing the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_create_new_book(self):
        # Functionalities 5: Create New Book
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()

        # Fill out the new book form
        self.driver.find_element(By.NAME, 'title').send_keys("Test Book")
        self.driver.find_element(By.NAME, 'author').send_keys("Test Author")
        self.driver.find_element(By.NAME, 'content').send_keys("This is a test book content.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify that the book is saved and redirected to My Books Page
        self.assertIn("My Books", self.driver.title)

    def test_view_my_books(self):
        # Functionalities 6: View My Books
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        self.assertIn("My Books", self.driver.title)

    def test_view_book_details(self):
        # Functionalities 7: View Book Details
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        self.driver.find_element(By.XPATH, '//a[contains(text(), "View")]').click()
        self.assertIn("Book Details", self.driver.title)

    def test_navigate_back_to_my_books(self):
        # Functionalities 8: Navigate Back to My Books Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        self.driver.find_element(By.XPATH, '//a[contains(text(), "View")]').click()
        self.driver.find_element(By.LINK_TEXT, 'Back to My Books').click()
        self.assertIn("My Books", self.driver.title)

    def test_view_about_page(self):
        # Functionalities 9: View About Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'About').click()
        self.assertIn("About", self.driver.title)

    def test_data_storage(self):
        # Functionalities 10: Data Storage using Text Files
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        self.driver.find_element(By.NAME, 'title').send_keys("Test Book")
        self.driver.find_element(By.NAME, 'author').send_keys("Test Author")
        self.driver.find_element(By.NAME, 'content').send_keys("This is a test book content.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Check if the book is saved in the text file
        with open('books.txt', 'r') as f:
            books = f.readlines()
            self.assertIn("Test Book|Test Author|This is a test book content.\n", books)

        # Clean up by removing the test book from the file
        with open('books.txt', 'w') as f:
            for book in books:
                if "Test Book" not in book:
                    f.write(book)

if __name__ == '__main__':
    unittest.main()
