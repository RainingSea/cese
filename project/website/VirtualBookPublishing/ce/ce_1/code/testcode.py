import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestVirtualBookPublishingApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8455/')  # Access the login page

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

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("user1", "user123")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
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
        self.assertIn("Login", self.driver.title)

    def test_access_dashboard(self):
        # Functionalities 4: Test accessing the Dashboard Page
        self.login("user1", "user123")
        self.assertIn("Dashboard", self.driver.title)

    def test_create_new_book(self):
        # Functionalities 5: Test creating a new book
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the new book form
        self.driver.find_element(By.NAME, 'title').send_keys("My New Book")
        self.driver.find_element(By.NAME, 'author').send_keys("Author Name")
        self.driver.find_element(By.NAME, 'content').send_keys("This is the content of my new book.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for saving the book

        # Verify that the new book is displayed on the My Books page
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("My New Book", self.driver.page_source)

    def test_view_my_books(self):
        # Functionalities 6: Test viewing My Books
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("My Books", self.driver.title)

    def test_view_book_details(self):
        # Functionalities 7: Test viewing book details
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.XPATH, '//a[contains(text(), "My First Book")]').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Book Details", self.driver.title)

    def test_navigate_back_to_my_books(self):
        # Functionalities 8: Test navigation back to My Books
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.XPATH, '//a[contains(text(), "My First Book")]').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.LINK_TEXT, 'Back to My Books').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("My Books", self.driver.title)

    def test_view_about_page(self):
        # Functionalities 9: Test viewing the About Page
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'About').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("About", self.driver.title)

    def test_data_storage(self):
        # Functionalities 10: Test data storage using text files
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the new book form
        self.driver.find_element(By.NAME, 'title').send_keys("Test Book")
        self.driver.find_element(By.NAME, 'author').send_keys("Test Author")
        self.driver.find_element(By.NAME, 'content').send_keys("Test content for the book.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for saving the book

        # Verify that the book details are saved correctly
        with open('books.txt', 'r') as file:
            content = file.read()
            self.assertIn("Test Book", content)

if __name__ == '__main__':
    unittest.main()
