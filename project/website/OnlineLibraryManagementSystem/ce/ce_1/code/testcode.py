import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess
import os

class TestOnlineLibrarySystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8107/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.title_contains('Dashboard'))

    def test_1_user_registration(self):
        """Test user registration functionality"""
        username = "testuser_" + str(int(time.time()))
        password = "testpass123"
        
        # Fill registration form
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//form[@action="/register"]/button').click()
        
        # Verify redirect to dashboard
        self.wait.until(EC.title_contains('Dashboard'))
        self.assertIn('Welcome', self.driver.page_source)

    def test_2_user_login(self):
        """Test user login with valid credentials"""
        self.login("admin", "admin123")
        self.assertIn('Welcome, admin!', self.driver.page_source)

    def test_3_view_dashboard(self):
        """Test dashboard view after login"""
        self.login("admin", "admin123")
        
        # Verify navigation options
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, 'Book Management').is_displayed())
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, 'User Management').is_displayed())
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, 'Search Books').is_displayed())
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, 'Logout').is_displayed())
        
        # Verify statistics
        self.assertIn('Total Books:', self.driver.page_source)
        self.assertIn('Total Users:', self.driver.page_source)

    def test_4_manage_books(self):
        """Test book management functionality"""
        self.login("admin", "admin123")
        
        # Navigate to books page
        self.driver.find_element(By.LINK_TEXT, 'Book Management').click()
        self.wait.until(EC.title_contains('Book Management'))
        
        # Add a new book
        title = "Test Book " + str(int(time.time()))
        author = "Test Author"
        isbn = "1234567890"
        
        self.driver.find_element(By.NAME, 'title').send_keys(title)
        self.driver.find_element(By.NAME, 'author').send_keys(author)
        self.driver.find_element(By.NAME, 'isbn').send_keys(isbn)
        self.driver.find_element(By.XPATH, '//form[@action="/books"]/button').click()
        
        # Verify book appears in the list
        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), title))
        
        # Delete the book
        delete_link = self.driver.find_element(By.XPATH, f'//td[text()="{isbn}"]/following-sibling::td/a')
        delete_link.click()
        
        # Verify book is removed
        self.wait.until_not(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), title))

    def test_5_manage_user_accounts(self):
        """Test user management functionality"""
        self.login("admin", "admin123")
        
        # Navigate to users page
        self.driver.find_element(By.LINK_TEXT, 'User Management').click()
        self.wait.until(EC.title_contains('User Management'))
        
        # Add a new user
        username = "testuser_" + str(int(time.time()))
        password = "testpass123"
        
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//form[@action="/users"]/button').click()
        
        # Verify user appears in the list
        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), username))

    def test_6_search_books(self):
        """Test book search functionality"""
        self.login("admin", "admin123")
        
        # Navigate to search page
        self.driver.find_element(By.LINK_TEXT, 'Search Books').click()
        self.wait.until(EC.title_contains('Search Books'))
        
        # Search for existing book
        self.driver.find_element(By.NAME, 'query').send_keys('Great Gatsby')
        self.driver.find_element(By.XPATH, '//form[@action="/search"]/button').click()
        
        # Verify search results
        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'The Great Gatsby'))

    def test_7_user_logout(self):
        """Test logout functionality"""
        self.login("admin", "admin123")
        
        # Click logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        
        # Verify redirect to login page
        self.wait.until(EC.title_contains('Login'))
        self.assertIn('Library System - Login', self.driver.page_source)

    def test_8_file_handling(self):
        """Test data storage in files"""
        # Check initial books file
        with open('books.txt', 'r') as f:
            books = f.readlines()
            self.assertGreater(len(books), 0)
            
        # Check initial users file
        with open('users.txt', 'r') as f:
            users = f.readlines()
            self.assertGreater(len(users), 0)

if __name__ == '__main__':
    unittest.main()
