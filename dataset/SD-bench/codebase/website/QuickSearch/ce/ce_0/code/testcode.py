import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestQuickSearchApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8680/')  # Navigate to the login page

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
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)

        # Verify the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter valid username and password, then submit
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Expect an error message (not implemented in the codebase)
        self.fail("Error message for existing username not implemented")

    def test_user_login(self):
        # Verify the Login form is displayed
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("admin", "admin123")

        # Verify redirection to Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8680/')  # Navigate back to login
        self.login("invalid_user", "wrong_password")

        # Expect an error message (not implemented in the codebase)
        self.fail("Error message for invalid credentials not implemented")

    def test_search_for_specific_words(self):
        # Login and navigate to Dashboard
        self.login("admin", "admin123")

        # Verify the search bar is displayed
        search_bar = self.driver.find_element(By.NAME, 'query')
        self.assertIsNotNone(search_bar)

        # Enter a specific word and submit
        search_bar.send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify search results
        results = self.driver.find_elements(By.CLASS_NAME, 'card-title')
        self.assertGreater(len(results), 0, "No search results found.")

        # Enter a non-existent word
        search_bar = self.driver.find_element(By.NAME, 'query')
        search_bar.clear()
        search_bar.send_keys("nonexistentbook")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Expect a message indicating no results (not implemented in the codebase)
        self.fail("No results message not implemented")

    def test_view_book_details(self):
        # Login and search for a book
        self.login("admin", "admin123")
        search_bar = self.driver.find_element(By.NAME, 'query')
        search_bar.send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Click on a book to view details
        self.driver.find_element(By.LINK_TEXT, 'View Details').click()
        time.sleep(1)

        # Verify Book Details Page
        self.assertIn("1984", self.driver.title)

    def test_add_books_to_reading_list(self):
        # Navigate to Book Details Page
        self.login("admin", "admin123")
        search_bar = self.driver.find_element(By.NAME, 'query')
        search_bar.send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'View Details').click()
        time.sleep(1)

        # Click 'Add to Reading List'
        self.driver.find_element(By.LINK_TEXT, 'Add to Reading List').click()
        time.sleep(1)

        # Expect confirmation message (not implemented in the codebase)
        self.fail("Confirmation message for adding to reading list not implemented")

    def test_view_and_manage_reading_list(self):
        # Login and navigate to Reading List Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Reading List').click()
        time.sleep(1)

        # Verify Reading List is displayed
        books = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(books), 0, "Reading list is empty.")

        # Remove a book from the reading list
        self.driver.find_element(By.LINK_TEXT, 'Remove').click()
        time.sleep(1)

        # Expect updated reading list (not implemented in the codebase)
        self.fail("Removing book from reading list not implemented")

    def test_user_logout(self):
        # Login and logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access Dashboard after logout
        self.driver.get('http://localhost:8680/dashboard')
        time.sleep(1)

        # Expect redirection to Login Page (not implemented in the codebase)
        self.fail("Access control after logout not implemented")

    def test_navigate_back_to_dashboard(self):
        # Login and navigate to Book Details Page
        self.login("admin", "admin123")
        search_bar = self.driver.find_element(By.NAME, 'query')
        search_bar.send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'View Details').click()
        time.sleep(1)

        # Click back to Dashboard
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)

        # Verify redirection to Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

    def test_view_detailed_information(self):
        # Login and search for a book
        self.login("admin", "admin123")
        search_bar = self.driver.find_element(By.NAME, 'query')
        search_bar.send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Click on a book to view details
        self.driver.find_element(By.LINK_TEXT, 'View Details').click()
        time.sleep(1)

        # Verify detailed information is displayed
        self.assertIn("1984", self.driver.page_source)
        self.assertIn("George Orwell", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
