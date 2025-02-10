import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestBookWormSearchApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8589/')

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
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

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Check for error message (not implemented in codebase)
        self.fail("Error message for existing username not implemented")

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Perform login with valid credentials
        self.login("admin", "admin123")

        # Verify redirection to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Perform login with invalid credentials
        self.driver.get('http://localhost:8589/')
        self.login("invalid_user", "invalid_pass")

        # Check for error message (not implemented in codebase)
        self.fail("Error message for invalid login not implemented")

    def test_book_search(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify the Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Search for a valid book title
        self.driver.find_element(By.NAME, 'search').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify search results are displayed
        search_results = self.driver.find_elements(By.LINK_TEXT, '1984')
        self.assertGreater(len(search_results), 0, "No search results found.")

        # Search for a non-existing book
        self.driver.find_element(By.NAME, 'search').clear()
        self.driver.find_element(By.NAME, 'search').send_keys("NonExistingBook")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Check for no results message (not implemented in codebase)
        self.fail("No results message not implemented")

    def test_view_book_details(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click on a book to view details
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)

        # Verify the Book Details Page is displayed
        self.assertIn("Book Details", self.driver.title)

        # Check for book description and author details
        book_details = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("George Orwell", book_details)
        self.assertIn("dystopian social science fiction novel", book_details)

    def test_add_book_to_reading_list(self):
        # Login and navigate to the Book Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)

        # Add the book to the reading list
        self.driver.find_element(By.XPATH, '//a[text()="Add to Reading List"]').click()
        time.sleep(1)

        # Navigate to the Reading List Page
        self.driver.find_element(By.LINK_TEXT, 'Reading List').click()
        time.sleep(1)

        # Verify the book is in the reading list
        reading_list = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("1984", reading_list)

    def test_view_and_manage_reading_list(self):
        # Login and navigate to the Reading List Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Reading List').click()
        time.sleep(1)

        # Verify the Reading List Page is displayed
        self.assertIn("Your Reading List", self.driver.title)

        # Remove a book from the reading list
        self.driver.find_element(By.XPATH, '//a[text()="Remove"]').click()
        time.sleep(1)

        # Verify the book is removed from the reading list
        reading_list = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn("To Kill a Mockingbird", reading_list)

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page
        self.driver.get('http://localhost:8589/dashboard')
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # Add a book to the reading list and log out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//a[text()="Add to Reading List"]').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Log back in and verify the book is still in the reading list
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Reading List').click()
        time.sleep(1)
        reading_list = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("1984", reading_list)

        # Modify the reading list
        self.driver.find_element(By.XPATH, '//a[text()="Remove"]').click()
        time.sleep(1)

        # Verify changes in the local text files (not implemented in codebase)
        self.fail("Data integrity check not implemented")

if __name__ == '__main__':
    unittest.main()
