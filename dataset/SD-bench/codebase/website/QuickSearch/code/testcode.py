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
        self.driver.get('http://localhost:8685/')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter new user details
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.ID, 'username').send_keys(new_username)
        self.driver.find_element(By.ID, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'username').send_keys("admin")
        self.driver.find_element(By.ID, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message is displayed
        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertIn("Username already exists", error_message)

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Test invalid login
        self.driver.get('http://localhost:8685/')
        self.login("invalid_user", "invalid_pass")

        # Verify error message is displayed
        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertIn("Invalid credentials", error_message)

    def test_search_books(self):
        # Test search functionality
        self.login("admin", "admin123")

        # Verify search bar is present
        search_bar = self.driver.find_element(By.NAME, 'search')
        self.assertIsNotNone(search_bar)

        # Enter search query
        search_bar.send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify search results
        results = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(results), 0, "No search results found.")

        # Test search with no results
        search_bar.clear()
        search_bar.send_keys("Nonexistent Book")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify no results message
        no_results_message = self.driver.find_element(By.CLASS_NAME, 'alert-info').text
        self.assertIn("No books found", no_results_message)

    def test_view_book_details(self):
        # Test viewing book details
        self.login("admin", "admin123")

        # Click on a book link
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)

        # Verify book details page
        self.assertIn("Book Details", self.driver.title)
        book_title = self.driver.find_element(By.TAG_NAME, 'h2').text
        self.assertEqual(book_title, "1984")

    def test_add_to_reading_list(self):
        # Test adding a book to the reading list
        self.login("admin", "admin123")

        # Navigate to book details
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)

        # Click 'Add to Reading List'
        self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()
        time.sleep(1)

        # Verify confirmation message
        confirmation_message = self.driver.find_element(By.CLASS_NAME, 'alert-success').text
        self.assertIn("added to your reading list", confirmation_message)

        # Navigate to reading list
        self.driver.find_element(By.LINK_TEXT, 'View Reading List').click()
        time.sleep(1)

        # Verify book is in reading list
        reading_list_books = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(reading_list_books), 0, "Reading list is empty.")

    def test_view_and_manage_reading_list(self):
        # Test viewing and managing the reading list
        self.login("admin", "admin123")

        # Navigate to reading list
        self.driver.find_element(By.LINK_TEXT, 'View Reading List').click()
        time.sleep(1)

        # Verify reading list is displayed
        reading_list_books = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(reading_list_books), 0, "Reading list is empty.")

        # Remove a book from the reading list
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        time.sleep(1)

        # Verify book is removed
        updated_reading_list_books = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertLess(len(updated_reading_list_books), len(reading_list_books), "Book was not removed.")

    def test_user_logout(self):
        # Test user logout functionality
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8685/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Test navigating back to the Dashboard
        self.login("admin", "admin123")

        # Navigate to book details
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)

        # Click 'Back to Dashboard'
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)

        # Verify redirection to Dashboard
        self.assertIn("Dashboard", self.driver.title)

    def test_view_detailed_information(self):
        # Test viewing detailed information of a book
        self.login("admin", "admin123")

        # Click on a book link
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)

        # Verify detailed information is displayed
        book_title = self.driver.find_element(By.TAG_NAME, 'h2').text
        self.assertEqual(book_title, "1984")
        book_author = self.driver.find_element(By.XPATH, '//p/strong[text()="Author:"]/following-sibling::text()').text
        self.assertEqual(book_author, "George Orwell")

if __name__ == '__main__':
    unittest.main()
