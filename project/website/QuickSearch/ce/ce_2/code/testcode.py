import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestBookApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8228/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.get('http://localhost:8228/register')
        
        # Enter valid username and password
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8228/register')
        self.driver.find_element(By.NAME, 'username').send_keys('admin')  # existing username
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message
        self.assertIn("Registration failed", self.driver.page_source)

    def test_user_login(self):
        # Test valid login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Test invalid login
        self.driver.get('http://localhost:8228/')
        self.login("admin", "wrongpassword")
        self.assertIn("Login failed", self.driver.page_source)

    def test_search_books(self):
        # Login first
        self.login("admin", "admin123")
        
        # Search for a book
        search_box = self.driver.find_element(By.NAME, 'query')
        search_box.send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify search results
        self.assertIn("1984", self.driver.page_source)

        # Search for a non-existing book
        search_box.clear()
        search_box.send_keys("NonExistingBook")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.assertIn("No results were found", self.driver.page_source)

    def test_view_book_details(self):
        # Login first
        self.login("admin", "admin123")
        
        # Search for a book and click on it
        self.driver.find_element(By.NAME, 'query').send_keys("The Great Gatsby")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.driver.find_element(By.LINK_TEXT, "The Great Gatsby").click()

        # Verify book details
        self.assertIn("The Great Gatsby", self.driver.page_source)
        self.assertIn("F. Scott Fitzgerald", self.driver.page_source)

    def test_add_to_reading_list(self):
        # Login first
        self.login("admin", "admin123")
        
        # Search for a book and add it to reading list
        self.driver.find_element(By.NAME, 'query').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.driver.find_element(By.LINK_TEXT, "1984").click()
        self.driver.find_element(By.LINK_TEXT, "Add to Reading List").click()

        # Verify that the book is added to the reading list
        self.driver.get('http://localhost:8228/reading_list')
        self.assertIn("1984", self.driver.page_source)

    def test_view_reading_list(self):
        # Login first
        self.login("admin", "admin123")
        
        # Navigate to reading list
        self.driver.get('http://localhost:8228/reading_list')
        self.assertIn("Your Reading List", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
