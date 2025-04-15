import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestWebApplication(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8325/') 

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
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8325/register')
        
        # Verify registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Register a new user
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify successful registration
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8325/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertIn("Username already taken", error_message)

    def test_user_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8325/')
        
        # Verify login form is displayed
        self.assertIn("Login", self.driver.title)

        # Login with valid credentials
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Login with invalid credentials
        self.driver.get('http://localhost:8325/')
        self.login("invalid_user", "wrong_password")
        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertIn("Invalid credentials", error_message)

    def test_search_books(self):
        # Functionality 3: Search for Specific Words or Phrases
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8325/dashboard')

        # Verify search bar is displayed
        search_bar = self.driver.find_element(By.NAME, 'search')
        self.assertIsNotNone(search_bar)

        # Search for an existing book
        search_bar.send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        search_results = self.driver.find_elements(By.XPATH, '//ul/li')
        self.assertGreater(len(search_results), 0)

        # Search for a non-existing book
        search_bar.clear()
        search_bar.send_keys("NonExistingBook")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        search_results = self.driver.find_elements(By.XPATH, '//ul/li')
        self.assertEqual(len(search_results), 0)

    def test_view_book_details(self):
        # Functionality 4: View Book Details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8325/dashboard')

        # Click on a book to view details
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        self.assertIn("1984", self.driver.title)

        # Verify detailed information is displayed
        book_details = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("George Orwell", book_details)
        self.assertIn("A dystopian novel about totalitarianism.", book_details)

    def test_add_books_to_reading_list(self):
        # Functionality 5: Add Books to Reading List
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8325/book/1984')

        # Add book to reading list
        self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()
        
        # Verify book is added to reading list
        self.driver.get('http://localhost:8325/reading_list')
        reading_list = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("1984", reading_list)

    def test_view_and_manage_reading_list(self):
        # Functionality 6: View and Manage Reading List
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8325/reading_list')

        # Verify reading list is displayed
        reading_list = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("The Great Gatsby", reading_list)

        # Remove a book from the reading list (not implemented in codebase)
        self.fail("Remove book functionality not implemented")

    def test_user_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8325/dashboard')

        # Logout
        self.driver.find_element(By.XPATH, '//button[text()="Logout"]').click()
        self.assertIn("Login", self.driver.title)

        # Attempt to access dashboard after logout
        self.driver.get('http://localhost:8325/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 8: Navigate Back to Dashboard
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8325/book/1984')

        # Navigate back to dashboard
        self.driver.back()
        self.assertIn("Dashboard", self.driver.title)

    def test_view_detailed_information(self):
        # Functionality 9: View Detailed Information
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8325/dashboard')

        # Click on 'Details' for a specific book
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        self.assertIn("1984", self.driver.title)

        # Verify detailed information is displayed
        book_details = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("George Orwell", book_details)
        self.assertIn("A dystopian novel about totalitarianism.", book_details)

if __name__ == '__main__':
    unittest.main()
