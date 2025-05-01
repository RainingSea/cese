import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestBookWormApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8561/')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.get('http://localhost:8561/login')
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.title_contains('Dashboard'))

    def test_1_user_registration(self):
        # Test registration page display
        self.driver.get('http://localhost:8561/register')
        self.assertIn('Register', self.driver.title)
        self.assertTrue(self.driver.find_element(By.NAME, 'username'))
        self.assertTrue(self.driver.find_element(By.NAME, 'password'))
        
        # Test successful registration
        username = "testuser_" + str(int(time.time()))
        password = "testpass123"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.wait.until(EC.title_contains('Login'))
        
        # Test duplicate registration
        self.driver.get('http://localhost:8561/register')
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        error_message = self.driver.find_element(By.CSS_SELECTOR, 'p[style="color:red"]')
        self.assertEqual(error_message.text, 'Username already exists')

    def test_2_user_login(self):
        # Test login page display
        self.driver.get('http://localhost:8561/login')
        self.assertIn('Login', self.driver.title)
        self.assertTrue(self.driver.find_element(By.NAME, 'username'))
        self.assertTrue(self.driver.find_element(By.NAME, 'password'))
        
        # Test successful login
        self.login('admin', 'admin123')
        self.assertIn('Dashboard', self.driver.title)
        
        # Test invalid login
        self.driver.get('http://localhost:8561/login')
        self.driver.find_element(By.NAME, 'username').send_keys('wronguser')
        self.driver.find_element(By.NAME, 'password').send_keys('wrongpass')
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        error_message = self.driver.find_element(By.CSS_SELECTOR, 'p[style="color:red"]')
        self.assertEqual(error_message.text, 'Invalid credentials')

    def test_3_book_search(self):
        self.login('admin', 'admin123')
        
        # Test search with results
        search_input = self.driver.find_element(By.NAME, 'query')
        search_input.send_keys('Great')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        results = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(results), 0)
        
        # Test search with no results
        search_input = self.driver.find_element(By.NAME, 'query')
        search_input.clear()
        search_input.send_keys('Nonexistent Book')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        results = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(results), 0)

    def test_4_view_book_details(self):
        self.login('admin', 'admin123')
        
        # Search for a book first
        search_input = self.driver.find_element(By.NAME, 'query')
        search_input.send_keys('Great')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        # Click on the first result
        first_result = self.driver.find_element(By.TAG_NAME, 'a')
        first_result.click()
        
        # Verify book details page
        self.wait.until(EC.title_contains('The Great Gatsby'))
        title = self.driver.find_element(By.TAG_NAME, 'h1').text
        author = self.driver.find_element(By.TAG_NAME, 'h2').text
        description = self.driver.find_element(By.TAG_NAME, 'p').text
        
        self.assertEqual(title, 'The Great Gatsby')
        self.assertTrue('F. Scott Fitzgerald' in author)
        self.assertTrue('American Dream' in description)

    def test_5_add_book_to_reading_list(self):
        self.login('admin', 'admin123')
        
        # Search for a book first
        search_input = self.driver.find_element(By.NAME, 'query')
        search_input.send_keys('Pride')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        # Click on the first result
        first_result = self.driver.find_element(By.TAG_NAME, 'a')
        first_result.click()
        
        # Add to reading list
        add_button = self.driver.find_element(By.LINK_TEXT, 'Add to Reading List')
        add_button.click()
        
        # Verify book was added by checking reading list
        reading_list_link = self.driver.find_element(By.LINK_TEXT, 'My Reading List')
        reading_list_link.click()
        
        books = self.driver.find_elements(By.TAG_NAME, 'li')
        found = False
        for book in books:
            if 'Pride and Prejudice' in book.text:
                found = True
                break
        self.assertTrue(found)

    def test_6_view_and_manage_reading_list(self):
        self.login('admin', 'admin123')
        
        # Go to reading list
        reading_list_link = self.driver.find_element(By.LINK_TEXT, 'My Reading List')
        reading_list_link.click()
        
        # Verify initial reading list
        books = self.driver.find_elements(By.TAG_NAME, 'li')
        initial_count = len(books)
        self.assertGreater(initial_count, 0)
        
        # Remove a book
        remove_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[style="color:red"]')
        if remove_links:
            remove_links[0].click()
            
            # Verify book was removed
            books_after_removal = self.driver.find_elements(By.TAG_NAME, 'li')
            self.assertEqual(len(books_after_removal), initial_count - 1)

    def test_7_user_logout(self):
        self.login('admin', 'admin123')
        
        # Logout
        logout_link = self.driver.find_element(By.LINK_TEXT, 'Logout')
        logout_link.click()
        
        # Verify redirected to login page
        self.wait.until(EC.title_contains('Login'))
        
        # Try to access dashboard directly
        self.driver.get('http://localhost:8561/dashboard')
        self.wait.until(EC.title_contains('Login'))

    def test_8_local_data_storage(self):
        # Test data persistence after logout/login
        self.login('admin', 'admin123')
        
        # Add a book to reading list
        search_input = self.driver.find_element(By.NAME, 'query')
        search_input.send_keys('Hobbit')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        first_result = self.driver.find_element(By.TAG_NAME, 'a')
        first_result.click()
        add_button = self.driver.find_element(By.LINK_TEXT, 'Add to Reading List')
        add_button.click()
        
        # Logout and login again
        logout_link = self.driver.find_element(By.LINK_TEXT, 'Logout')
        logout_link.click()
        self.login('admin', 'admin123')
        
        # Check reading list
        reading_list_link = self.driver.find_element(By.LINK_TEXT, 'My Reading List')
        reading_list_link.click()
        
        # Verify the book is still in the list
        books = self.driver.find_elements(By.TAG_NAME, 'li')
        found = False
        for book in books:
            if 'The Hobbit' in book.text:
                found = True
                break
        self.assertTrue(found)

if __name__ == '__main__':
    unittest.main()
