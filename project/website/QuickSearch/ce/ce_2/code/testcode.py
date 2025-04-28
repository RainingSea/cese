import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestBookApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8400/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8400/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8400/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()

        # Verify error message for existing username
        self.assertIn("User already exists!", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8400/')
        self.login("admin", "wrong_password")
        self.assertIn("Invalid credentials!", self.driver.page_source)

    def test_search_books(self):
        # Functionality 3: Search for Specific Words or Phrases
        self.login("admin", "admin123")  # Login first
        self.assertIn("Dashboard", self.driver.title)

        # Search for a book
        search_query = "1984"
        self.driver.find_element(By.NAME, 'query').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//input[@value="Search"]').click()

        # Verify search results
        self.assertIn("1984", self.driver.page_source)

        # Search for a non-existing book
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys("Nonexistent Book")
        self.driver.find_element(By.XPATH, '//input[@value="Search"]').click()
        self.assertIn("No results found", self.driver.page_source)

    def test_view_book_details(self):
        # Functionality 4: View Book Details
        self.login("admin", "admin123")  # Login first
        self.driver.find_element(By.LINK_TEXT, "1984 by George Orwell").click()  # Click on the book link

        # Verify book details
        self.assertIn("1984", self.driver.page_source)
        self.assertIn("George Orwell", self.driver.page_source)

    def test_add_to_reading_list(self):
        # Functionality 5: Add Books to Reading List
        self.login("user1", "user123")  # Login first
        self.driver.find_element(By.LINK_TEXT, "The Great Gatsby by F. Scott Fitzgerald").click()  # Click on the book link
        self.driver.find_element(By.XPATH, '//input[@value="Add to Reading List"]').click()

        # Verify that the book is added to the reading list
        self.driver.get('http://localhost:8400/reading_list')
        self.assertIn("The Great Gatsby", self.driver.page_source)

    def test_view_reading_list(self):
        # Functionality 6: View and Manage Reading List
        self.login("user1", "user123")  # Login first
        self.driver.get('http://localhost:8400/reading_list')

        # Verify that the reading list is displayed
        self.assertIn("Your Reading List", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Login first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 8: Navigate Back to Dashboard
        self.login("admin", "admin123")  # Login first
        self.driver.find_element(By.LINK_TEXT, "1984 by George Orwell").click()  # Click on the book link
        self.driver.find_element(By.LINK_TEXT, "Back to Dashboard").click()

        # Verify that the user is back on the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

if __name__ == '__main__':
    unittest.main()
