import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import os

class TestOnlineLibraryManagementSystem(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8666/')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Functionalities 1: User Registration
        self.fail("User registration functionality not implemented")

    def test_user_login(self):
        # Functionalities 2: User Login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_view_dashboard(self):
        # Functionalities 3: View Dashboard
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)
        nav_links = self.driver.find_elements(By.TAG_NAME, 'a')
        nav_texts = [link.text for link in nav_links]
        self.assertIn("Book Management", nav_texts)
        self.assertIn("User Management", nav_texts)
        self.assertIn("Search Books", nav_texts)

    def test_manage_books(self):
        # Functionalities 4: Manage Books
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Book Management').click()
        self.driver.find_element(By.ID, 'title').send_keys("New Book")
        self.driver.find_element(By.ID, 'author').send_keys("New Author")
        self.driver.find_element(By.XPATH, '//button[@value="Add"]').click()
        self.assertIn("New Book by New Author", self.driver.page_source)

    def test_manage_user_accounts(self):
        # Functionalities 5: Manage User Accounts
        self.fail("User management functionality not implemented")

    def test_search_books(self):
        # Functionalities 6: Search Books
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Search Books').click()
        self.driver.find_element(By.ID, 'query').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.assertIn("1984 by George Orwell", self.driver.page_source)

    def test_user_logout(self):
        # Functionalities 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_file_handling_for_data_storage(self):
        # Functionalities 8: File Handling for Data Storage
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Book Management').click()
        self.driver.find_element(By.ID, 'title').send_keys("File Book")
        self.driver.find_element(By.ID, 'author').send_keys("File Author")
        self.driver.find_element(By.XPATH, '//button[@value="Add"]').click()
        
        # Check if the book is added in the file
        with open('books.txt', 'r') as file:
            books = file.read()
            self.assertIn("File Book|File Author", books)
        
        # Delete the book
        self.driver.find_element(By.ID, 'title').send_keys("File Book")
        self.driver.find_element(By.XPATH, '//button[@value="Delete"]').click()

        # Check if the book is removed from the file
        with open('books.txt', 'r') as file:
            books = file.read()
            self.assertNotIn("File Book|File Author", books)

if __name__ == '__main__':
    unittest.main()
