import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestBookWormSearch(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8591/')

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
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Check for error message (not implemented in codebase)
        self.fail("Error message for existing username not implemented")

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("admin", "admin123")

        # Verify redirection to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8591/')
        self.login("invalid_user", "invalid_pass")

        # Check for error message (not implemented in codebase)
        self.fail("Error message for invalid login not implemented")

    def test_book_search(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Enter a valid book title
        self.driver.find_element(By.NAME, 'query').send_keys('1984')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify search results
        self.assertIn("1984 by George Orwell", self.driver.page_source)

        # Enter a non-matching keyword
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys('Nonexistent Book')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Check for no results message (not implemented in codebase)
        self.fail("No results message not implemented")

    def test_view_book_details(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click on a book from the search results
        self.driver.find_element(By.LINK_TEXT, '1984 by George Orwell').click()
        time.sleep(1)

        # Verify the Book Details Page
        self.assertIn("1984", self.driver.title)
        self.assertIn("George Orwell", self.driver.page_source)
        self.assertIn("A dystopian novel about totalitarianism.", self.driver.page_source)

    def test_add_book_to_reading_list(self):
        # Navigate to the Book Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, '1984 by George Orwell').click()
        time.sleep(1)

        # Add to Reading List (button not implemented in codebase)
        self.fail("Add to Reading List button not implemented")

    def test_view_and_manage_reading_list(self):
        # Login and navigate to the Reading List Page
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'My Reading List').click()
        time.sleep(1)

        # Verify the Reading List Page
        self.assertIn("My Reading List", self.driver.title)
        self.assertIn("The Great Gatsby", self.driver.page_source)

        # Remove a book (functionality not implemented in codebase)
        self.fail("Remove book from reading list not implemented")

    def test_user_logout(self):
        # Login and logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access Dashboard
        self.driver.get('http://localhost:8591/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # Add a book to the reading list and verify persistence
        self.fail("Local data storage test not implemented")

if __name__ == '__main__':
    unittest.main()
