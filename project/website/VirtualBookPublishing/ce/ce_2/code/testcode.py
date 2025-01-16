import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import os

class TestVirtualBookPublishingApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8691/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and stop the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
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
        # Functionalities 4: Test accessing the Dashboard Page
        self.login("admin", "admin123")
        # Verify that the Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.title)

    def test_create_new_book(self):
        # Functionalities 5: Test creating a new book
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        # Verify that the Create New Book Page is displayed
        self.assertIn("Create New Book", self.driver.title)
        # Enter book details
        self.driver.find_element(By.NAME, 'title').send_keys("New Book")
        self.driver.find_element(By.NAME, 'author').send_keys("Author Name")
        self.driver.find_element(By.NAME, 'content').send_keys("Book Content")
        self.driver.find_element(By.XPATH, '//button[text()="Create Book"]').click()
        # Verify redirection to My Books Page
        self.assertIn("My Books", self.driver.title)

    def test_view_my_books(self):
        # Functionalities 6: Test viewing My Books
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'My Books').click()
        # Verify that the My Books Page is displayed
        self.assertIn("My Books", self.driver.title)

    def test_view_book_details(self):
        # Functionalities 7: Test viewing book details
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'My Books').click()
        # Click on the first book link
        self.driver.find_element(By.XPATH, '//ul/li/a').click()
        # Verify that the Book Details Page is displayed
        self.assertIn("Book Details", self.driver.title)

    def test_navigate_back_to_my_books(self):
        # Functionalities 8: Test navigating back to My Books Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'My Books').click()
        self.driver.find_element(By.XPATH, '//ul/li/a').click()
        # Click the back link
        self.driver.find_element(By.LINK_TEXT, 'Back to My Books').click()
        # Verify redirection back to My Books Page
        self.assertIn("My Books", self.driver.title)

    def test_view_about_page(self):
        # Functionalities 9: Test viewing the About Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'About').click()
        # Verify that the About Page is displayed
        self.assertIn("About", self.driver.title)

    def test_data_storage(self):
        # Functionalities 10: Test data storage
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        self.driver.find_element(By.NAME, 'title').send_keys("Storage Test Book")
        self.driver.find_element(By.NAME, 'author').send_keys("Test Author")
        self.driver.find_element(By.NAME, 'content').send_keys("Test Content")
        self.driver.find_element(By.XPATH, '//button[text()="Create Book"]').click()
        # Check if the book is saved in the text file
        with open('books.txt', 'r') as file:
            content = file.read()
            self.assertIn("Storage Test Book|Test Author|Test Content", content)
        # Delete the text file and check error handling
        os.remove('books.txt')
        self.driver.find_element(By.LINK_TEXT, 'My Books').click()
        # Verify error message is displayed
        self.assertIn("Error", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
