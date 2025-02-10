import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestQuickSearchApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8683/') 

    def tearDown(self):
        # Close the web driver session and stop the Flask app
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
        time.sleep(1)  # Wait for the next page to load

        # Verify the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8683/')
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)

    def test_search_for_specific_words(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify the search bar is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Enter a specific word or phrase in the search bar and submit
        # Note: The search functionality is not implemented in the codebase
        self.fail("Search functionality not implemented")

    def test_view_book_details(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click on a book from the search results
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the Book Details Page is displayed
        self.assertIn("The Great Gatsby", self.driver.title)

    def test_add_books_to_reading_list(self):
        # Login and navigate to the Book Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)  # Wait for the next page to load

        # Click the 'Add to Reading List' button
        # Note: The functionality to add to the reading list is not implemented in the codebase
        self.fail("Add to reading list functionality not implemented")

    def test_view_and_manage_reading_list(self):
        # Login and navigate to the Reading List Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8683/reading_list')

        # Verify the user's reading list is displayed
        self.assertIn("Reading List", self.driver.title)

        # Remove a book from the reading list
        # Note: The functionality to remove a book is not implemented in the codebase
        self.fail("Remove book from reading list functionality not implemented")

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Logout from the Dashboard Page
        # Note: The logout functionality is not implemented in the codebase
        self.fail("Logout functionality not implemented")

    def test_navigate_back_to_dashboard(self):
        # Login and navigate to the Book Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)  # Wait for the next page to load

        # Click the back button to return to the Dashboard Page
        self.driver.back()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected back to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

    def test_view_detailed_information(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click the 'Details' button for a specific book
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the detailed information for that book is displayed
        self.assertIn("The Great Gatsby", self.driver.title)

if __name__ == '__main__':
    unittest.main()
