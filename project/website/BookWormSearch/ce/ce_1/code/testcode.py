import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestBookWormSearch(unittest.TestCase):

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
        self.driver.get('http://localhost:8562/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the webdriver
        self.driver.quit()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.url_contains('dashboard'))

    def logout(self):
        # Helper method to perform logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.url_contains('login'))

    def test_1_user_registration(self):
        """Test user registration functionality"""
        # Navigate to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.title_contains('Register'))
        
        # Test successful registration
        username = "testuser"
        password = "testpass123"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.wait.until(EC.url_contains('dashboard'))
        
        # Verify registration by logging out and logging back in
        self.logout()
        self.login(username, password)
        self.assertIn('Dashboard', self.driver.title)
        self.logout()
        
        # Test registration with existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        error_message = self.driver.find_element(By.CLASS_NAME, 'error').text
        self.assertEqual(error_message, "Username already exists")

    def test_2_user_login(self):
        """Test user login functionality"""
        # Test successful login
        self.login("admin", "admin123")
        self.assertIn('Dashboard', self.driver.title)
        self.logout()
        
        # Test login with invalid credentials
        self.driver.find_element(By.NAME, 'username').send_keys('wronguser')
        self.driver.find_element(By.NAME, 'password').send_keys('wrongpass')
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        error_message = self.driver.find_element(By.CLASS_NAME, 'error').text
        self.assertEqual(error_message, "Invalid credentials")

    def test_3_book_search(self):
        """Test book search functionality"""
        self.login("admin", "admin123")
        
        # Test search with valid query
        search_input = self.driver.find_element(By.NAME, 'query')
        search_input.send_keys('Great Gatsby')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'book-card')))
        book_cards = self.driver.find_elements(By.CLASS_NAME, 'book-card')
        self.assertGreater(len(book_cards), 0)
        
        # Test search with no results
        search_input = self.driver.find_element(By.NAME, 'query')
        search_input.clear()
        search_input.send_keys('Nonexistent Book')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for search to complete
        book_cards = self.driver.find_elements(By.CLASS_NAME, 'book-card')
        self.assertEqual(len(book_cards), 0)

    def test_4_view_book_details(self):
        """Test viewing book details"""
        self.login("admin", "admin123")
        
        # Search for a book first
        search_input = self.driver.find_element(By.NAME, 'query')
        search_input.send_keys('Great Gatsby')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'book-card')))
        
        # Click on the book details link
        self.driver.find_element(By.LINK_TEXT, 'View Details').click()
        self.wait.until(EC.title_contains('The Great Gatsby'))
        
        # Verify book details are displayed
        book_title = self.driver.find_element(By.TAG_NAME, 'h2').text
        book_author = self.driver.find_element(By.TAG_NAME, 'h3').text
        self.assertEqual(book_title, 'The Great Gatsby')
        self.assertIn('F. Scott Fitzgerald', book_author)

    def test_5_add_book_to_reading_list(self):
        """Test adding book to reading list"""
        self.login("admin", "admin123")
        
        # Search for a book first
        search_input = self.driver.find_element(By.NAME, 'query')
        search_input.send_keys('Mockingbird')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'book-card')))
        
        # Go to book details
        self.driver.find_element(By.LINK_TEXT, 'View Details').click()
        self.wait.until(EC.title_contains('To Kill a Mockingbird'))
        
        # Add to reading list
        self.driver.find_element(By.LINK_TEXT, 'Add to Reading List').click()
        self.wait.until(EC.url_contains('reading_list'))
        
        # Verify book is in reading list
        book_titles = [el.text for el in self.driver.find_elements(By.TAG_NAME, 'h3')]
        self.assertIn('To Kill a Mockingbird', book_titles)

    def test_6_view_and_manage_reading_list(self):
        """Test viewing and managing reading list"""
        self.login("admin", "admin123")
        
        # Go directly to reading list
        self.driver.find_element(By.LINK_TEXT, 'Reading List').click()
        self.wait.until(EC.url_contains('reading_list'))
        
        # Check initial reading list
        initial_books = self.driver.find_elements(By.CLASS_NAME, 'book-card')
        
        # Remove a book if exists
        if len(initial_books) > 0:
            remove_links = self.driver.find_elements(By.LINK_TEXT, 'Remove')
            if len(remove_links) > 0:
                remove_links[0].click()
                self.wait.until(EC.url_contains('reading_list'))
                updated_books = self.driver.find_elements(By.CLASS_NAME, 'book-card')
                self.assertEqual(len(updated_books), len(initial_books) - 1)

    def test_7_user_logout(self):
        """Test user logout functionality"""
        self.login("admin", "admin123")
        self.logout()
        
        # Verify logout by trying to access dashboard
        self.driver.get('http://localhost:8562/dashboard')
        self.wait.until(EC.url_contains('login'))
        self.assertIn('Login', self.driver.title)

    def test_8_local_data_storage(self):
        """Test data persistence in local storage"""
        # First login and add a book to reading list
        self.login("user1", "password1")
        
        # Go to reading list and note initial count
        self.driver.find_element(By.LINK_TEXT, 'Reading List').click()
        self.wait.until(EC.url_contains('reading_list'))
        initial_books = self.driver.find_elements(By.CLASS_NAME, 'book-card')
        
        # Logout and login again
        self.logout()
        self.login("user1", "password1")
        
        # Go to reading list again and verify count is same
        self.driver.find_element(By.LINK_TEXT, 'Reading List').click()
        self.wait.until(EC.url_contains('reading_list'))
        current_books = self.driver.find_elements(By.CLASS_NAME, 'book-card')
        self.assertEqual(len(current_books), len(initial_books))

if __name__ == '__main__':
    unittest.main()
