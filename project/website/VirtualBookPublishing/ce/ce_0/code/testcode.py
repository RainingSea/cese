import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import os

class TestVirtualBookPublishing(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8689/login')

    def tearDown(self):
        # Close the web driver session and terminate the application process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigation to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.assertIn("Login", self.driver.page_source)

    def test_access_dashboard(self):
        # Functionalities 4: Accessing the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Welcome, admin", self.driver.page_source)

    def test_create_new_book(self):
        # Functionalities 5: Create New Book
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        self.assertIn("Create New Book", self.driver.page_source)

        self.driver.find_element(By.NAME, 'title').send_keys("New Book")
        self.driver.find_element(By.NAME, 'author').send_keys("Author Name")
        self.driver.find_element(By.NAME, 'content').send_keys("Content of the new book")
        self.driver.find_element(By.XPATH, '//button[text()="Create Book"]').click()
        self.assertIn("My Books", self.driver.page_source)

    def test_view_my_books(self):
        # Functionalities 6: View My Books
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'My Books').click()
        self.assertIn("My Books", self.driver.page_source)

    def test_view_book_details(self):
        # Functionalities 7: View Book Details
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'My Books').click()
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        self.assertIn("The Great Gatsby", self.driver.page_source)

    def test_navigate_back_to_my_books(self):
        # Functionalities 8: Navigate Back to My Books Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'My Books').click()
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        self.driver.find_element(By.LINK_TEXT, 'Back to My Books').click()
        self.assertIn("My Books", self.driver.page_source)

    def test_view_about_page(self):
        # Functionalities 9: View About Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'About').click()
        self.assertIn("About This Application", self.driver.page_source)

    def test_data_storage_using_text_files(self):
        # Functionalities 10: Data Storage using Text Files
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        self.driver.find_element(By.NAME, 'title').send_keys("Test Book")
        self.driver.find_element(By.NAME, 'author').send_keys("Test Author")
        self.driver.find_element(By.NAME, 'content').send_keys("Test Content")
        self.driver.find_element(By.XPATH, '//button[text()="Create Book"]').click()

        # Check if the book is saved in the text file
        with open('books.txt', 'r') as f:
            self.assertIn("Test Book|Test Author|Test Content", f.read())

        # Delete the text file and check for error handling
        os.remove('books.txt')
        self.driver.find_element(By.LINK_TEXT, 'My Books').click()
        self.assertIn("My Books", self.driver.page_source)  # Expecting an error message

if __name__ == '__main__':
    unittest.main()
