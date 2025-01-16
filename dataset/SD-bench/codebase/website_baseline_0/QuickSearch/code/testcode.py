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
        self.driver.get('http://localhost:8549/')

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
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the registration page to load

        # Verify registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("username is already taken", self.driver.page_source)

    def test_user_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify redirection to Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Test invalid login
        self.driver.get('http://localhost:8549/')
        self.login("invalid_user", "wrong_password")

        # Verify error message for invalid credentials
        self.assertIn("credentials are incorrect", self.driver.page_source)

    def test_search_functionality(self):
        # Functionality 3: Search for Specific Words or Phrases
        self.login("admin", "admin123")

        # Verify search bar is displayed
        self.assertTrue(self.driver.find_element(By.NAME, 'search'))

        # Perform a search
        search_query = "Gatsby"
        self.driver.find_element(By.NAME, 'search').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify search results
        self.assertIn("The Great Gatsby", self.driver.page_source)

        # Test search with no results
        self.driver.find_element(By.NAME, 'search').clear()
        self.driver.find_element(By.NAME, 'search').send_keys("Nonexistent Book")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify no results message
        self.assertIn("no results were found", self.driver.page_source)

    def test_view_book_details(self):
        # Functionality 4: View Book Details
        self.login("admin", "admin123")

        # Navigate to book details
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)

        # Verify book details page
        self.assertIn("The Great Gatsby", self.driver.title)
        self.assertIn("F. Scott Fitzgerald", self.driver.page_source)

    def test_add_books_to_reading_list(self):
        # Functionality 5: Add Books to Reading List
        self.login("admin", "admin123")

        # Navigate to book details
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)

        # Add to reading list
        self.driver.find_element(By.LINK_TEXT, 'Add to Reading List').click()
        time.sleep(1)

        # Verify confirmation message
        self.assertIn("added to your reading list", self.driver.page_source)

    def test_view_and_manage_reading_list(self):
        # Functionality 6: View and Manage Reading List
        self.login("admin", "admin123")

        # Navigate to reading list
        self.driver.find_element(By.LINK_TEXT, 'Reading List').click()
        time.sleep(1)

        # Verify reading list
        self.assertIn("Your Reading List", self.driver.title)

        # Remove a book from reading list
        # Assuming there's a remove button for each book
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        time.sleep(1)

        # Verify book is removed
        self.assertNotIn("The Great Gatsby", self.driver.page_source)

    def test_user_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")

        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to access dashboard after logout
        self.driver.get('http://localhost:8549/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 8: Navigate Back to Dashboard
        self.login("admin", "admin123")

        # Navigate to book details
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)

        # Navigate back to dashboard
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)

        # Verify redirection to dashboard
        self.assertIn("Dashboard", self.driver.title)

    def test_view_detailed_information(self):
        # Functionality 9: View Detailed Information
        self.login("admin", "admin123")

        # Navigate to book details
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)

        # Verify detailed information
        self.assertIn("The Great Gatsby", self.driver.page_source)
        self.assertIn("F. Scott Fitzgerald", self.driver.page_source)
        self.assertIn("A novel set in the 1920s about the American dream.", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
