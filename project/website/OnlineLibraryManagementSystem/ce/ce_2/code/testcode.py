import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestLibraryManagementSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8108/')
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)

    def test_1_user_registration(self):
        """Test user registration functionality"""
        # Click register button
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        
        # Fill registration form
        username = "testuser"
        password = "testpass"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        
        # Verify redirect to dashboard
        self.assertIn("Dashboard", self.driver.title)

    def test_2_user_login(self):
        """Test user login functionality"""
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_3_view_dashboard(self):
        """Test dashboard view after login"""
        self.login("admin", "admin123")
        
        # Verify navigation options are present
        nav_links = self.driver.find_elements(By.XPATH, '//header/a')
        self.assertEqual(len(nav_links), 5)  # Dashboard, Books, Users, Search, Logout
        
        # Verify welcome message
        welcome_text = self.driver.find_element(By.XPATH, '//header/span').text
        self.assertIn("admin", welcome_text)

    def test_4_manage_books(self):
        """Test book management functionality"""
        self.login("admin", "admin123")
        
        # Navigate to books page
        self.driver.find_element(By.LINK_TEXT, 'Books').click()
        time.sleep(1)
        
        # Add a new book
        title = "Test Book"
        author = "Test Author"
        isbn = "1234567890"
        self.driver.find_element(By.NAME, 'title').send_keys(title)
        self.driver.find_element(By.NAME, 'author').send_keys(author)
        self.driver.find_element(By.NAME, 'isbn').send_keys(isbn)
        self.driver.find_element(By.XPATH, '//button[text()="Add Book"]').click()
        time.sleep(1)
        
        # Verify book appears in the list
        books_table = self.driver.find_element(By.TAG_NAME, 'table')
        self.assertIn(title, books_table.text)
        
        # Delete the book
        delete_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Delete"]')
        delete_buttons[-1].click()  # Click the last delete button (our new book)
        time.sleep(1)
        
        # Verify book is removed
        books_table = self.driver.find_element(By.TAG_NAME, 'table')
        self.assertNotIn(title, books_table.text)

    def test_5_manage_user_accounts(self):
        """Test user management functionality"""
        self.login("admin", "admin123")
        
        # Navigate to users page
        self.driver.find_element(By.LINK_TEXT, 'Users').click()
        time.sleep(1)
        
        # Verify existing users are listed
        users_table = self.driver.find_element(By.TAG_NAME, 'table')
        self.assertIn("admin", users_table.text)
        self.assertIn("user1", users_table.text)

    def test_6_search_books(self):
        """Test book search functionality"""
        self.login("admin", "admin123")
        
        # Navigate to search page
        self.driver.find_element(By.LINK_TEXT, 'Search').click()
        time.sleep(1)
        
        # Search for existing book
        self.driver.find_element(By.NAME, 'query').send_keys("Great Gatsby")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)
        
        # Verify search results
        results_table = self.driver.find_element(By.TAG_NAME, 'table')
        self.assertIn("The Great Gatsby", results_table.text)

    def test_7_user_logout(self):
        """Test logout functionality"""
        self.login("admin", "admin123")
        
        # Click logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        
        # Verify redirect to login page
        self.assertIn("Login", self.driver.title)
        
        # Verify navigation links are gone
        nav_links = self.driver.find_elements(By.XPATH, '//header/a')
        self.assertEqual(len(nav_links), 0)

    def test_8_file_handling(self):
        """Test data storage in files"""
        # Check initial books file
        with open('books.txt', 'r') as f:
            books_content = f.read()
            self.assertIn("The Great Gatsby", books_content)
            self.assertIn("To Kill a Mockingbird", books_content)
        
        # Check initial users file
        with open('users.txt', 'r') as f:
            users_content = f.read()
            self.assertIn("admin,admin123", users_content)
            self.assertIn("user1,password1", users_content)

if __name__ == '__main__':
    unittest.main()
