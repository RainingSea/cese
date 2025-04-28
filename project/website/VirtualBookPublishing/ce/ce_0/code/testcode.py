import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import os

class TestVirtualBookPublishingApp(unittest.TestCase):

    def setUp(self):
        # Start the server and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/') 

    def tearDown(self):
        # Close the web driver session and terminate the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

    def test_login(self):
        # Functionalities 1: User Login
        self.login("user1", "user123")
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
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_access_dashboard(self):
        # Functionalities 4: Accessing the Dashboard Page
        self.login("user1", "user123")
        self.assertIn("Dashboard", self.driver.title)

    def test_create_new_book(self):
        # Functionalities 5: Create New Book
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        
        # Fill out the new book form
        self.driver.find_element(By.NAME, 'title').send_keys("My New Book")
        self.driver.find_element(By.NAME, 'author').send_keys("Author Test")
        self.driver.find_element(By.NAME, 'content').send_keys("This is the content of my new book.")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify that the user is redirected to the My Books Page
        self.assertIn("My Published Books", self.driver.page_source)

    def test_view_my_books(self):
        # Functionalities 6: View My Books
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        self.assertIn("My Published Books", self.driver.page_source)

    def test_view_book_details(self):
        # Functionalities 7: View Book Details
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        # Assuming there's a button to view details next to the book
        self.driver.find_element(By.XPATH, '//button[text()="View"]').click()
        self.assertIn("Book Details", self.driver.title)

    def test_navigate_back_to_my_books(self):
        # Functionalities 8: Navigate Back to My Books Page
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'View My Books').click()
        self.driver.find_element(By.XPATH, '//button[text()="Back"]').click()
        self.assertIn("My Published Books", self.driver.page_source)

    def test_view_about_page(self):
        # Functionalities 9: View About Page
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'About').click()
        self.assertIn("About VirtualBookPublishing", self.driver.title)

    def test_data_storage(self):
        # Functionalities 10: Data Storage using Text Files
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Book').click()
        self.driver.find_element(By.NAME, 'title').send_keys("Test Book")
        self.driver.find_element(By.NAME, 'author').send_keys("Test Author")
        self.driver.find_element(By.NAME, 'content').send_keys("Test content.")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Check if the book is saved in the text file
        with open(os.path.join(os.path.dirname(__file__), 'books.txt'), 'r') as file:
            content = file.read()
            self.assertIn("Test Book", content)

if __name__ == '__main__':
    unittest.main()
