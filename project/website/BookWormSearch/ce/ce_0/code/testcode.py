import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestBookWormSearchApp(unittest.TestCase):

    def setUp(self):
        # Start the main application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8289/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the application process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8289/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8289/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that an error message is displayed
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8289/')  # Navigate to Login Page
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Invalid login
        self.driver.get('http://localhost:8289/')  # Navigate to Login Page
        self.login("admin", "wrongpassword")
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.title)  # Should still be on login page

    def test_book_search(self):
        # Functionality 3: Book Search
        self.login("admin", "admin123")  # Log in successfully
        self.driver.get('http://localhost:8289/dashboard')  # Navigate to Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Search for a valid book
        search_query = "1984"
        self.driver.find_element(By.NAME, 'query').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the results to load
        self.assertIn("1984", self.driver.page_source)  # Check if the book is in the results

        # Search for a non-existing book
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys("Nonexistent Book")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the results to load
        self.assertIn("No results found", self.driver.page_source)  # Check for no results message

    def test_view_reading_list(self):
        # Functionality 6: View and Manage Reading List
        self.login("admin", "admin123")  # Log in successfully
        self.driver.get('http://localhost:8289/reading_list')  # Navigate to Reading List Page
        self.assertIn("My Reading List", self.driver.title)

        # Check if the reading list is displayed
        self.assertIn("Reading List", self.driver.page_source)  # Check if the reading list is displayed

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Log in successfully
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_data_storage(self):
        # Functionality 8: Local Data Storage
        self.login("admin", "admin123")  # Log in successfully
        self.driver.get('http://localhost:8289/reading_list')  # Navigate to Reading List Page

        # Check if the reading list is empty initially
        self.assertIn("My Reading List", self.driver.page_source)

        # Add a book to the reading list (this part is not implemented in the codebase)
        self.fail("Add Book to Reading List functionality not implemented")

if __name__ == '__main__':
    unittest.main()
