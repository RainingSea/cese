import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestVirtualBookPublishingApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the web application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

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
        self.login("user1", "password1")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
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
        self.login("user1", "password1")
        self.assertIn("Dashboard", self.driver.title)

    def test_create_new_book(self):
        # Functionalities 5: Test creating a new book
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the new book form
        self.driver.find_element(By.NAME, 'title').send_keys("New Book Title")
        self.driver.find_element(By.NAME, 'author').send_keys("New Author")
        self.driver.find_element(By.NAME, 'content').send_keys("Content of the new book.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the book to be created

        # Verify that the book is displayed in My Books
        self.assertIn("New Book Title", self.driver.page_source)

    def test_view_my_books(self):
        # Functionalities 6: Test viewing My Books
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("My Published Books", self.driver.title)

    def test_view_book_details(self):
        # Functionalities 7: Test viewing book details
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.LINK_TEXT, 'New Book Title').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("New Book Title", self.driver.page_source)

    def test_navigate_back_to_my_books(self):
        # Functionalities 8: Test navigating back to My Books
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.LINK_TEXT, 'New Book Title').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.LINK_TEXT, 'Back to My Books').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("My Published Books", self.driver.title)

    def test_view_about_page(self):
        # Functionalities 9: Test viewing About Page
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'About').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("About Virtual Book Publishing", self.driver.title)

    def test_data_storage(self):
        # Functionalities 10: Test data storage using text files
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the new book form
        self.driver.find_element(By.NAME, 'title').send_keys("Test Book Title")
        self.driver.find_element(By.NAME, 'author').send_keys("Test Author")
        self.driver.find_element(By.NAME, 'content').send_keys("Content of the test book.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the book to be created

        # Verify that the book is saved in the text file
        with open('books.txt', 'r') as file:
            content = file.read()
            self.assertIn("Test Book Title|Test Author|Content of the test book.", content)

if __name__ == '__main__':
    unittest.main()
