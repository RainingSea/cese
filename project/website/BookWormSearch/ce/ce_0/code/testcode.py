import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestBookWormSearch(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8992/login')

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
        # Navigate to the Registration Page
        self.driver.get('http://localhost:8992/register')
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8992/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that an error message is displayed
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Logout to test invalid login
        self.driver.get('http://localhost:8992/logout')
        time.sleep(1)

        # Enter invalid credentials
        self.login("invalid_user", "invalid_pass")
        self.assertIn("Login", self.driver.title)

    def test_book_search(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Search for a valid book title
        self.driver.find_element(By.NAME, 'query').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for search results

        # Verify search results
        self.assertIn("1984", self.driver.page_source)

        # Search for a non-existent book
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys("NonExistentBook")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for search results

        # Verify no results found
        self.assertNotIn("NonExistentBook", self.driver.page_source)

    def test_view_book_details(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Search and click on a book
        self.driver.find_element(By.NAME, 'query').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for search results
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)  # Wait for book details page

        # Verify book details
        self.assertIn("1984", self.driver.page_source)
        self.assertIn("George Orwell", self.driver.page_source)

    def test_add_book_to_reading_list(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Search and add a book to the reading list
        self.driver.find_element(By.NAME, 'query').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for search results
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)  # Wait for book details page
        self.driver.find_element(By.LINK_TEXT, 'Add to Reading List').click()
        time.sleep(1)  # Wait for redirection

        # Navigate to the Reading List Page
        self.driver.get('http://localhost:8992/reading_list')
        time.sleep(1)  # Wait for the page to load

        # Verify the book is in the reading list
        self.assertIn("1984", self.driver.page_source)

    def test_view_and_manage_reading_list(self):
        # Login and navigate to the Reading List Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8992/reading_list')
        time.sleep(1)  # Wait for the page to load

        # Verify the reading list is displayed
        self.assertIn("Your Reading List", self.driver.page_source)

        # Remove a book from the reading list (not implemented in the codebase)
        # This test will fail as the functionality is not implemented
        self.fail("Remove book from reading list functionality not implemented")

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Logout
        self.driver.get('http://localhost:8992/logout')
        time.sleep(1)  # Wait for redirection

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the Dashboard Page
        self.driver.get('http://localhost:8992/dashboard')
        time.sleep(1)  # Wait for redirection

        # Verify redirection back to the login page
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # Login and add a book to the reading list
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'query').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for search results
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)  # Wait for book details page
        self.driver.find_element(By.LINK_TEXT, 'Add to Reading List').click()
        time.sleep(1)  # Wait for redirection

        # Logout and log back in
        self.driver.get('http://localhost:8992/logout')
        time.sleep(1)
        self.login("admin", "admin123")

        # Navigate to the Reading List Page
        self.driver.get('http://localhost:8992/reading_list')
        time.sleep(1)  # Wait for the page to load

        # Verify the book is still in the reading list
        self.assertIn("1984", self.driver.page_source)

        # Modify the reading list (not implemented in the codebase)
        # This test will fail as the functionality is not implemented
        self.fail("Modify reading list functionality not implemented")

if __name__ == '__main__':
    unittest.main()
