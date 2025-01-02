import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestVirtualBookPublishing(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'], cwd='D:/Project/CE/CE/project/website/VirtualBookPublishing/ce/ce_1/code')
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8157')

    def tearDown(self):
        # Close the web driver session and stop the Flask application
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
        self.login("admin1", "pass123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
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

        # Enter book details and submit the form
        self.driver.find_element(By.NAME, 'title').send_keys("New Book Title")
        self.driver.find_element(By.NAME, 'author').send_keys("New Author")
        self.driver.find_element(By.NAME, 'content').send_keys("This is the content of the new book.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
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

        # Click on a book to view details
        self.driver.find_element(By.LINK_TEXT, 'My First Book').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Book Details Page is displayed
        self.assertIn("Book Details", self.driver.title)

    def test_navigate_back_to_my_books(self):
        # Functionalities 8: Test navigating back to My Books Page
        self.login("admin1", "pass123")

        # Navigate to My Books Page
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load

        # Click on a book to view details
        self.driver.find_element(By.LINK_TEXT, 'My First Book').click()
        time.sleep(1)  # Wait for the next page to load

        # Click the back navigation link
        self.driver.find_element(By.LINK_TEXT, 'Back to My Books').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected back to the My Books Page
        self.assertIn("My Books", self.driver.title)

    def test_data_storage(self):
        # Functionalities 10: Test data storage using text files
        self.login("admin1", "pass123")

        # Navigate to Create New Book Page
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        time.sleep(1)  # Wait for the next page to load

        # Enter book details and submit the form
        book_title = "Storage Test Book"
        self.driver.find_element(By.NAME, 'title').send_keys(book_title)
        self.driver.find_element(By.NAME, 'author').send_keys("Storage Author")
        self.driver.find_element(By.NAME, 'content').send_keys("This is the content of the storage test book.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the book details are saved in the text file
        with open('D:/Project/CE/CE/project/website/VirtualBookPublishing/ce/ce_1/code/books.txt', 'r') as file:
            content = file.read()
            self.assertIn(book_title, content)

        # Delete the text file and verify error handling
        os.remove('D:/Project/CE/CE/project/website/VirtualBookPublishing/ce/ce_1/code/books.txt')
        self.driver.get('http://localhost:8157/my_books')
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Book not found.", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
