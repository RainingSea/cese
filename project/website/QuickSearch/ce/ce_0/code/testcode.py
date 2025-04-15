import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestQuickSearchApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8321/') 

    def tearDown(self):
        # Close the web driver session
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
        self.driver.get('http://localhost:8321/register')
        
        # Verify registration form is displayed
        self.assertTrue(self.driver.find_element(By.NAME, 'username').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'password').is_displayed())

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify registration success
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8321/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message
        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertIn("Username already taken", error_message)

    def test_user_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify redirection to Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Attempt login with invalid credentials
        self.driver.get('http://localhost:8321/')
        self.login("invalid_user", "invalid_pass")

        # Verify error message
        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertIn("credentials are incorrect", error_message)

    def test_search_books(self):
        # Functionality 3: Search for Specific Words or Phrases
        self.login("admin", "admin123")

        # Verify search bar is displayed
        self.assertTrue(self.driver.find_element(By.NAME, 'query').is_displayed())

        # Search for a specific book
        self.driver.find_element(By.NAME, 'query').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for search results

        # Verify search results
        search_results = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(search_results), 0)

        # Search for a non-existent book
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys("NonExistentBook")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for search results

        # Verify no results message
        no_results_message = self.driver.find_element(By.TAG_NAME, 'ul').text
        self.assertIn("No results found", no_results_message)

    def test_view_book_details(self):
        # Functionality 4: View Book Details
        self.login("admin", "admin123")

        # Navigate to book details
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)  # Wait for book details page

        # Verify book details are displayed
        book_title = self.driver.find_element(By.TAG_NAME, 'h2').text
        self.assertEqual(book_title, "1984")

    def test_add_books_to_reading_list(self):
        # Functionality 5: Add Books to Reading List
        self.login("admin", "admin123")

        # Navigate to book details and add to reading list
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)  # Wait for book details page
        self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()
        time.sleep(1)  # Wait for redirection

        # Verify book is added to reading list
        self.driver.get('http://localhost:8321/reading_list')
        reading_list_books = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertIn("1984", [book.text for book in reading_list_books])

    def test_view_and_manage_reading_list(self):
        # Functionality 6: View and Manage Reading List
        self.login("admin", "admin123")

        # Navigate to reading list
        self.driver.get('http://localhost:8321/reading_list')

        # Verify reading list is displayed
        reading_list_books = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(reading_list_books), 0)

        # Remove a book from the reading list
        # Assuming there is a remove button next to each book
        # This functionality is not implemented in the codebase, hence failing the test
        self.fail("Remove functionality not implemented")

    def test_user_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")

        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for redirection

        # Verify redirection to Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access Dashboard Page after logout
        self.driver.get('http://localhost:8321/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 8: Navigate Back to Dashboard
        self.login("admin", "admin123")

        # Navigate to book details and back to dashboard
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)  # Wait for book details page
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)  # Wait for dashboard page

        # Verify redirection to Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

    def test_view_detailed_information(self):
        # Functionality 9: View Detailed Information
        self.login("admin", "admin123")

        # Navigate to book details
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)  # Wait for book details page

        # Verify detailed information is displayed
        book_details = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("1984", book_details)
        self.assertIn("George Orwell", book_details)
        self.assertIn("A dystopian novel about totalitarianism and surveillance.", book_details)

if __name__ == '__main__':
    unittest.main()
