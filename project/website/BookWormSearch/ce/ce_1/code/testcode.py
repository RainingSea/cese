import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestBookWormSearchApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8300/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
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
        self.driver.get('http://localhost:8300/register')
        self.assertIn("Register", self.driver.title)

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8300/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check for error message
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8300/')
        self.login("admin", "wrong_password")
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.title)

    def test_book_search(self):
        # Functionality 3: Book Search
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Search for a valid book
        search_query = "1984"
        self.driver.find_element(By.NAME, 'query').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the results to load
        self.assertIn("1984", self.driver.page_source)

        # Search for a non-existent book
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys("Nonexistent Book")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the results to load
        self.assertIn("No results found", self.driver.page_source)

    def test_view_book_details(self):
        # Functionality 4: View Book Details
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "1984").click()
        time.sleep(1)  # Wait for the book details to load
        self.assertIn("1984", self.driver.page_source)

    def test_add_to_reading_list(self):
        # Functionality 5: Add Book to Reading List
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "1984").click()
        self.driver.find_element(By.LINK_TEXT, "Add to Reading List").click()
        time.sleep(1)  # Wait for the action to complete

        # Verify the book is in the reading list
        self.driver.get('http://localhost:8300/reading_list')
        time.sleep(1)  # Wait for the reading list to load
        self.assertIn("1984", self.driver.page_source)

    def test_view_reading_list(self):
        # Functionality 6: View and Manage Reading List
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8300/reading_list')
        time.sleep(1)  # Wait for the reading list to load
        self.assertIn("My Reading List", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.title)

    def test_data_storage(self):
        # Functionality 8: Local Data Storage
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "1984").click()
        self.driver.find_element(By.LINK_TEXT, "Add to Reading List").click()
        time.sleep(1)  # Wait for the action to complete
        self.driver.get('http://localhost:8300/logout')
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8300/reading_list')
        time.sleep(1)  # Wait for the reading list to load
        self.assertIn("1984", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
