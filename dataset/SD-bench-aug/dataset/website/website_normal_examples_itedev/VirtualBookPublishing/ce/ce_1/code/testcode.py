import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestVirtualBookPublishingApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/login')

    def tearDown(self):
        # Close the web driver and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: User Login
        self.login("user1", "password1")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigation to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: User Registration
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
        # Functionalities 4: Accessing the Dashboard Page
        self.login("user1", "password1")
        self.assertIn("Welcome", self.driver.page_source)

    def test_create_new_book(self):
        # Functionalities 5: Create New Book
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the new book form
        self.driver.find_element(By.NAME, 'title').send_keys("New Book Title")
        self.driver.find_element(By.NAME, 'author').send_keys("New Author")
        self.driver.find_element(By.NAME, 'content').send_keys("Content of the new book.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the book to be saved

        # Verify that the book is listed in My Books
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("New Book Title", self.driver.page_source)

    def test_view_my_books(self):
        # Functionalities 6: View My Books
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("My Published Books", self.driver.page_source)

    def test_view_book_details(self):
        # Functionalities 7: View Book Details
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load

        # Click on the first book's link
        book_link = self.driver.find_element(By.XPATH, '//li/a')
        book_link.click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("New Book Title", self.driver.page_source)

    def test_navigate_back_to_my_books(self):
        # Functionalities 8: Navigate Back to My Books Page
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load

        # Click on the first book's link
        book_link = self.driver.find_element(By.XPATH, '//li/a')
        book_link.click()
        time.sleep(1)  # Wait for the next page to load

        # Navigate back to My Books
        self.driver.find_element(By.LINK_TEXT, 'Back to My Books').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("My Published Books", self.driver.page_source)

    def test_view_about_page(self):
        # Functionalities 9: View About Page
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'About').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("About Virtual Book Publishing", self.driver.page_source)

    def test_data_storage(self):
        # Functionalities 10: Data Storage using Text Files
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the new book form
        self.driver.find_element(By.NAME, 'title').send_keys("Test Book Title")
        self.driver.find_element(By.NAME, 'author').send_keys("Test Author")
        self.driver.find_element(By.NAME, 'content').send_keys("Content of the test book.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the book to be saved

        # Check if the book is saved in the text file
        with open('books.txt', 'r') as file:
            content = file.read()
            self.assertIn("Test Book Title", content)

        # Delete the books.txt file for testing error handling
        os.remove('books.txt')

        # Try to view My Books after deleting the file
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Error", self.driver.page_source)  # Assuming error message is displayed

if __name__ == '__main__':
    unittest.main()
