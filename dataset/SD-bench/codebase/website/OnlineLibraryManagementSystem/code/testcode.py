import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineLibraryManagementSystem(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8668/')

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
        # Functionalities 1: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Functionalities 2: User Login
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_view_dashboard(self):
        # Functionalities 3: View Dashboard
        self.login("admin", "admin123")

        # Verify that the Dashboard displays navigation options
        self.assertIn("Manage Books", self.driver.page_source)
        self.assertIn("Manage Users", self.driver.page_source)

    def test_manage_books(self):
        # Functionalities 4: Manage Books
        self.fail("Not implemented")

    def test_manage_user_accounts(self):
        # Functionalities 5: Manage User Accounts
        self.fail("Not implemented")

    def test_search_books(self):
        # Functionalities 6: Search Books
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8668/search_books?query=1984')
        time.sleep(1)  # Wait for the search results to load

        # Verify the search results display the book's details
        self.assertIn("1984 by George Orwell", self.driver.page_source)

    def test_user_logout(self):
        # Functionalities 7: User Logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_file_handling_for_data_storage(self):
        # Functionalities 8: File Handling for Data Storage
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
