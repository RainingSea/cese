import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestVirtualBookPublishingApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web app to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8145')

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

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin1", "pass123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_access_dashboard(self):
        # Functionalities 4: Test accessing the Dashboard Page
        self.login("admin1", "pass123")

        # Verify that the Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.title)

    def test_create_new_book(self):
        # Functionalities 5: Test creating a new book
        self.login("admin1", "pass123")

        # Navigate to Create New Book Page
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Create New Book Page is displayed
        self.assertIn("Create New Book", self.driver.title)

        # Fill out the new book form
        book_title = "New Book Title"
        book_author = "Author Name"
        book_content = "This is the content of the new book."

        self.driver.find_element(By.NAME, 'title').send_keys(book_title)
        self.driver.find_element(By.NAME, 'author').send_keys(book_author)
        self.driver.find_element(By.NAME, 'content').send_keys(book_content)
        self.driver.find_element(By.XPATH, '//button[text()="Create Book"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the My Books Page
        self.assertIn("My Books", self.driver.title)

    def test_view_my_books(self):
        # Functionalities 6: Test viewing My Books
        self.login("admin1", "pass123")

        # Navigate to My Books Page
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the My Books Page is displayed
        self.assertIn("My Books", self.driver.title)

    def test_view_book_details(self):
        # Functionalities 7: Test viewing book details
        self.login("admin1", "pass123")

        # Navigate to My Books Page
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load

        # Click on the first book to view details
        self.driver.find_element(By.XPATH, '//ul/li/a').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Book Details Page is displayed
        self.assertIn("Book Details", self.driver.title)

    def test_navigate_back_to_my_books(self):
        # Functionalities 8: Test navigation back to My Books Page
        self.login("admin1", "pass123")

        # Navigate to My Books Page
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load

        # Click on the first book to view details
        self.driver.find_element(By.XPATH, '//ul/li/a').click()
        time.sleep(1)  # Wait for the next page to load

        # Click the back link to return to My Books Page
        self.driver.find_element(By.LINK_TEXT, 'Back to My Books').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the My Books Page is displayed
        self.assertIn("My Books", self.driver.title)

    def test_view_about_page(self):
        # Functionalities 9: Test viewing the About Page
        self.login("admin1", "pass123")

        # Navigate to About Page
        self.driver.find_element(By.LINK_TEXT, 'About').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the About Page is displayed
        self.assertIn("About", self.driver.title)

    def test_data_storage(self):
        # Functionalities 10: Test data storage using text files
        self.login("admin1", "pass123")

        # Navigate to Create New Book Page
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the new book form
        book_title = "Storage Test Book"
        book_author = "Test Author"
        book_content = "This is a test book for storage."

        self.driver.find_element(By.NAME, 'title').send_keys(book_title)
        self.driver.find_element(By.NAME, 'author').send_keys(book_author)
        self.driver.find_element(By.NAME, 'content').send_keys(book_content)
        self.driver.find_element(By.XPATH, '//button[text()="Create Book"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the book details are saved in the text file
        with open('books.txt', 'r') as file:
            content = file.read()
            self.assertIn(book_title, content)

        # Delete the books.txt file
        os.remove('books.txt')

        # Try to navigate to My Books Page
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that an error message is displayed
        self.assertIn("Error", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
