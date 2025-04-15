import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestQuickSearchApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8323/') 

    def tearDown(self):
        # Close the web driver session and stop the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Functionality 1: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)

        # Check registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Register a new user
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertIn("Username already exists", error_message)

    def test_user_login(self):
        # Functionality 2: User Login
        # Check login form is displayed
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Invalid login
        self.driver.get('http://localhost:8323/')
        self.login("invalid_user", "invalid_pass")
        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertIn("Invalid credentials", error_message)

    def test_search_books(self):
        # Functionality 3: Search for Specific Words or Phrases
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Search for a book
        self.driver.find_element(By.NAME, 'search').send_keys('1984')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify search results
        results = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(results), 0, "No search results found.")

        # Search for a non-existent book
        self.driver.find_element(By.NAME, 'search').clear()
        self.driver.find_element(By.NAME, 'search').send_keys('NonExistentBook')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify no results message
        no_results_message = self.driver.find_element(By.TAG_NAME, 'ul').text
        self.assertIn("No results found", no_results_message)

    def test_view_book_details(self):
        # Functionality 4: View Book Details
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'search').send_keys('1984')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Click on a book to view details
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)

        # Verify book details page
        self.assertIn("1984", self.driver.title)
        book_details = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("George Orwell", book_details)

    def test_add_books_to_reading_list(self):
        # Functionality 5: Add Books to Reading List
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'search').send_keys('1984')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)

        # Add book to reading list
        self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()
        time.sleep(1)

        # Verify book is added to reading list
        self.driver.get('http://localhost:8323/reading_list')
        reading_list = self.driver.find_element(By.TAG_NAME, 'ul').text
        self.assertIn("1984", reading_list)

    def test_view_and_manage_reading_list(self):
        # Functionality 6: View and Manage Reading List
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8323/reading_list')
        time.sleep(1)

        # Verify reading list is displayed
        reading_list = self.driver.find_element(By.TAG_NAME, 'ul').text
        self.assertIn("The Great Gatsby", reading_list)

        # Note: Removing a book from the reading list is not implemented in the codebase

    def test_user_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to access dashboard after logout
        self.driver.get('http://localhost:8323/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 8: Navigate Back to Dashboard
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'search').send_keys('1984')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)

        # Navigate back to dashboard
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)

        # Verify redirection to dashboard
        self.assertIn("Dashboard", self.driver.title)

    def test_view_detailed_information(self):
        # Functionality 9: View Detailed Information
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'search').send_keys('1984')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)

        # Verify detailed information
        book_details = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("1984", book_details)
        self.assertIn("George Orwell", book_details)
        self.assertIn("A dystopian novel about totalitarianism.", book_details)

if __name__ == '__main__':
    unittest.main()
