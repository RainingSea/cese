import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestVirtualBookPublishing(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8314')

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

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("user1", "user123")
        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.page_source)

    def test_access_dashboard(self):
        # Functionalities 4: Test accessing the Dashboard Page
        self.login("user1", "user123")
        # Verify that the Dashboard Page is displayed
        self.assertIn("Welcome, user1", self.driver.page_source)

    def test_create_new_book(self):
        # Functionalities 5: Test creating a new book
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify Create New Book Page is displayed
        self.assertIn("Create New Book", self.driver.page_source)

        # Enter book details
        self.driver.find_element(By.NAME, 'title').send_keys("New Book")
        self.driver.find_element(By.NAME, 'author').send_keys("Author Name")
        self.driver.find_element(By.NAME, 'content').send_keys("Book content here.")
        self.driver.find_element(By.XPATH, '//button[text()="Create Book"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to My Books Page
        self.assertIn("My Books", self.driver.page_source)

    def test_view_my_books(self):
        # Functionalities 6: Test viewing My Books
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'My Books').click()
        time.sleep(1)  # Wait for the next page to load
        # Verify My Books Page is displayed
        self.assertIn("My Books", self.driver.page_source)

    def test_view_book_details(self):
        # Functionalities 7: Test viewing book details
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'My Books').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)  # Wait for the next page to load
        # Verify Book Details Page is displayed
        self.assertIn("The Great Gatsby", self.driver.page_source)

    def test_navigate_back_to_my_books(self):
        # Functionalities 8: Test navigating back to My Books Page
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'My Books').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.LINK_TEXT, 'Back to My Books').click()
        time.sleep(1)  # Wait for the next page to load
        # Verify redirection back to My Books Page
        self.assertIn("My Books", self.driver.page_source)

    def test_view_about_page(self):
        # Functionalities 9: Test viewing the About Page
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'About').click()
        time.sleep(1)  # Wait for the next page to load
        # Verify About Page is displayed
        self.assertIn("About", self.driver.page_source)

    def test_data_storage(self):
        # Functionalities 10: Test data storage using text files
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        time.sleep(1)  # Wait for the next page to load

        # Enter book details
        self.driver.find_element(By.NAME, 'title').send_keys("Storage Test Book")
        self.driver.find_element(By.NAME, 'author').send_keys("Storage Author")
        self.driver.find_element(By.NAME, 'content').send_keys("Storage content here.")
        self.driver.find_element(By.XPATH, '//button[text()="Create Book"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify book details are saved in the text file
        with open('books.txt', 'r') as file:
            content = file.read()
            self.assertIn("Storage Test Book", content)

        # Test deleting the text file
        os.remove('books.txt')
        self.driver.find_element(By.LINK_TEXT, 'My Books').click()
        time.sleep(1)  # Wait for the next page to load
        # Verify error message is displayed
        self.assertIn("My Books", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
