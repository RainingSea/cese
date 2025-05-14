import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import subprocess

class TestLibraryManagementSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the Flask application
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        # Stop the Flask application
        cls.process.terminate()

    def setUp(self):
        # Initialize the webdriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8105/')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the webdriver session
        self.driver.quit()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.title_contains("Dashboard"))

    def test_1_user_login(self):
        """Test user login functionality"""
        # Test with valid credentials
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Test navigation back to login when not authenticated
        self.driver.get('http://localhost:8105/books')
        self.assertIn("Login", self.driver.title)

    def test_2_view_dashboard(self):
        """Test viewing the dashboard after login"""
        self.login("admin", "admin123")
        
        # Verify dashboard elements
        nav_links = self.driver.find_elements(By.CSS_SELECTOR, 'nav ul li a')
        self.assertEqual(len(nav_links), 4)
        self.assertEqual(nav_links[0].text, "Book Management")
        self.assertEqual(nav_links[1].text, "User Management")
        self.assertEqual(nav_links[2].text, "Search Books")
        self.assertEqual(nav_links[3].text, "Logout")

    def test_3_manage_books(self):
        """Test book management functionality"""
        self.login("admin", "admin123")
        
        # Navigate to book management
        self.driver.find_element(By.LINK_TEXT, "Book Management").click()
        self.wait.until(EC.title_contains("Book Management"))
        
        # Add a new book
        title = "Test Book"
        author = "Test Author"
        isbn = "1234567890"
        
        self.driver.find_element(By.NAME, 'title').send_keys(title)
        self.driver.find_element(By.NAME, 'author').send_keys(author)
        self.driver.find_element(By.NAME, 'isbn').send_keys(isbn)
        self.driver.find_element(By.NAME, 'add_book').click()
        
        # Verify book was added
        books = self.driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
        found = False
        for book in books:
            if isbn in book.text:
                found = True
                break
        self.assertTrue(found, "New book was not added to the table")
        
        # Delete the book
        delete_buttons = self.driver.find_elements(By.NAME, 'delete_book')
        delete_buttons[-1].click()  # Click the last delete button (our new book)
        
        # Verify book was deleted
        books_after_delete = self.driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
        found = False
        for book in books_after_delete:
            if isbn in book.text:
                found = True
                break
        self.assertFalse(found, "Book was not deleted from the table")

    def test_4_manage_users(self):
        """Test user management functionality"""
        self.login("admin", "admin123")
        
        # Navigate to user management
        self.driver.find_element(By.LINK_TEXT, "User Management").click()
        self.wait.until(EC.title_contains("User Management"))
        
        # Get initial user count
        initial_users = self.driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
        
        # Add a new user
        username = "testuser"
        password = "testpass"
        
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Add User"]').click()
        
        # Verify user was added
        users_after_add = self.driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
        self.assertEqual(len(users_after_add), len(initial_users) + 1)
        
        # Verify the new user appears in the list
        found = False
        for user in users_after_add:
            if username in user.text:
                found = True
                break
        self.assertTrue(found, "New user was not added to the table")

    def test_5_search_books(self):
        """Test book search functionality"""
        self.login("admin", "admin123")
        
        # Navigate to search page
        self.driver.find_element(By.LINK_TEXT, "Search Books").click()
        self.wait.until(EC.title_contains("Search Books"))
        
        # Search for an existing book
        query = "Gatsby"
        self.driver.find_element(By.NAME, 'query').send_keys(query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        # Verify search results
        results = self.driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
        self.assertGreater(len(results), 0, "No search results found")
        self.assertIn("The Great Gatsby", self.driver.page_source)

    def test_6_user_logout(self):
        """Test logout functionality"""
        self.login("admin", "admin123")
        
        # Click logout
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        self.wait.until(EC.title_contains("Login"))
        
        # Verify we're on login page and can't access dashboard directly
        self.driver.get('http://localhost:8105/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_7_file_handling(self):
        """Test data storage in files"""
        # Check books.txt exists and has content
        self.assertTrue(os.path.exists('books.txt'), "books.txt does not exist")
        with open('books.txt', 'r') as f:
            content = f.read()
            self.assertGreater(len(content), 0, "books.txt is empty")
            self.assertIn("The Great Gatsby", content)
        
        # Check users.txt exists and has content
        self.assertTrue(os.path.exists('users.txt'), "users.txt does not exist")
        with open('users.txt', 'r') as f:
            content = f.read()
            self.assertGreater(len(content), 0, "users.txt is empty")
            self.assertIn("admin:admin123:admin", content)

if __name__ == '__main__':
    unittest.main()
