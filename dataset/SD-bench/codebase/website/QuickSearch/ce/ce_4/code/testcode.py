import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestQuickSearchApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8684/')  # Navigate to the login page

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
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        # Verify Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Check for error message (not implemented in the codebase)
        self.fail("Error message for existing username not implemented")

    def test_user_login(self):
        # Verify Login form is displayed
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("admin", "admin123")

        # Verify redirection to Dashboard
        self.assertIn("Dashboard", self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8684/')  # Go back to login page
        self.login("invalid_user", "wrong_password")

        # Check for error message (not implemented in the codebase)
        self.fail("Error message for invalid credentials not implemented")

    def test_search_books(self):
        # Login and navigate to Dashboard
        self.login("admin", "admin123")

        # Verify search bar is displayed
        self.assertTrue(self.driver.find_element(By.NAME, 'query'))

        # Search for a specific book
        self.driver.find_element(By.NAME, 'query').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify search results
        self.assertIn("1984", self.driver.page_source)

        # Search for a non-existent book
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys("NonExistentBook")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Check for no results message (not implemented in the codebase)
        self.fail("No results message not implemented")

    def test_view_book_details(self):
        # Login and navigate to Dashboard
        self.login("admin", "admin123")

        # Click on a book to view details
        self.driver.find_element(By.LINK_TEXT, '1984').click()

        # Verify book details are displayed
        self.assertIn("1984", self.driver.title)
        self.assertIn("George Orwell", self.driver.page_source)

    def test_add_books_to_reading_list(self):
        # Navigate to Book Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, '1984').click()

        # Click 'Add to Reading List'
        self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()

        # Check for confirmation message (not implemented in the codebase)
        self.fail("Confirmation message for adding to reading list not implemented")

    def test_view_and_manage_reading_list(self):
        # Login and navigate to Reading List Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'My Reading List').click()

        # Verify reading list is displayed
        self.assertIn("My Reading List", self.driver.title)

        # Attempt to remove a book (functionality not implemented)
        self.fail("Remove book from reading list functionality not implemented")

    def test_user_logout(self):
        # Login and logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify redirection to Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access Dashboard after logout
        self.driver.get('http://localhost:8684/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Navigate to Book Details Page and back to Dashboard
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()

        # Verify redirection to Dashboard
        self.assertIn("Dashboard", self.driver.title)

    def test_view_detailed_information(self):
        # Click 'Details' for a specific book
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, '1984').click()

        # Verify detailed information is displayed
        self.assertIn("1984", self.driver.title)
        self.assertIn("George Orwell", self.driver.page_source)
        self.assertIn("A dystopian novel about totalitarianism.", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
