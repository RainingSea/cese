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
        self.driver.get('http://localhost:8283/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
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
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
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
        self.assertIn("Dashboard", self.driver.title)

    def test_create_new_book(self):
        # Functionalities 5: Test creating a new book
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()

        # Fill out the new book form
        self.driver.find_element(By.NAME, 'title').send_keys("My New Book")
        self.driver.find_element(By.NAME, 'author').send_keys("Author Name")
        self.driver.find_element(By.NAME, 'content').send_keys("This is the content of my new book.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify that the book is saved and user is redirected to My Books Page
        self.assertIn("My Published Books", self.driver.title)

    def test_view_my_books(self):
        # Functionalities 6: Test viewing My Books Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        self.assertIn("My Published Books", self.driver.title)

    def test_view_book_details(self):
        # Functionalities 7: Test viewing book details
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        self.driver.find_element(By.LINK_TEXT, 'My New Book').click()  # Assuming the book was created
        self.assertIn("Book Details", self.driver.title)

    def test_navigate_back_to_my_books(self):
        # Functionalities 8: Test navigating back to My Books Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        self.driver.find_element(By.LINK_TEXT, 'My New Book').click()  # Assuming the book was created
        self.driver.find_element(By.LINK_TEXT, 'Back to My Books').click()
        self.assertIn("My Published Books", self.driver.title)

    def test_view_about_page(self):
        # Functionalities 9: Test viewing About Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'About').click()
        self.assertIn("About", self.driver.title)

    def test_data_storage(self):
        # Functionalities 10: Test data storage using text files
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        self.driver.find_element(By.NAME, 'title').send_keys("Test Book")
        self.driver.find_element(By.NAME, 'author').send_keys("Test Author")
        self.driver.find_element(By.NAME, 'content').send_keys("Test content for the book.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Check if the book is saved in the text file
        user_books_file = "admin_books.txt"  # Assuming the username is admin
        self.assertTrue(os.path.exists(user_books_file), "User books file does not exist.")

        # Clean up by removing the created book file
        os.remove(user_books_file)

if __name__ == '__main__':
    unittest.main()
