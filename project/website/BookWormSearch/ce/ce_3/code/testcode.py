import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestBookWormSearchApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8995/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
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

        # Verify that the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then click the "Register" button
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that an error message is displayed
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Verify that the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8995/')  # Navigate back to the login page
        self.login("invalid_user", "invalid_pass")

        # Verify that an error message is displayed
        self.assertIn("Login", self.driver.title)

    def test_book_search(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify that the Dashboard Page is displayed with a search bar
        self.assertIn("Dashboard", self.driver.title)

        # Enter a valid book title in the search bar and click the "Search" button
        self.driver.find_element(By.NAME, 'query').send_keys('1984')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        # Verify that a list of matching book results is displayed
        self.assertIn("1984", self.driver.page_source)

        # Enter a keyword that does not match any book titles or authors
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys('Nonexistent Book')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        # Verify that a message is displayed indicating no results were found
        self.assertNotIn("Nonexistent Book", self.driver.page_source)

    def test_view_book_details(self):
        # Login and search for a book
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'query').send_keys('1984')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        # Click on a book from the search results
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)  # Wait for the book details page to load

        # Verify that the Book Details Page is displayed
        self.assertIn("1984", self.driver.page_source)

        # Check if the Book Details Page contains a description and author details
        self.assertIn("George Orwell", self.driver.page_source)

    def test_add_book_to_reading_list(self):
        # Navigate to the Book Details Page for a specific book
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'query').send_keys('1984')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)  # Wait for the book details page to load

        # Click the "Add to Reading List" button
        self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()
        time.sleep(1)  # Wait for the action to complete

        # Navigate to the Reading List Page
        self.driver.get('http://localhost:8995/reading_list')
        time.sleep(1)  # Wait for the reading list page to load

        # Verify that the added book appears in the reading list
        self.assertIn("1984", self.driver.page_source)

    def test_view_and_manage_reading_list(self):
        # Login successfully and navigate to the Reading List Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8995/reading_list')
        time.sleep(1)  # Wait for the reading list page to load

        # Verify that the Reading List Page displays the user's current reading list
        self.assertIn("Your Reading List", self.driver.page_source)

        # Remove a book from the reading list
        self.driver.find_element(By.LINK_TEXT, 'Remove').click()
        time.sleep(1)  # Wait for the action to complete

        # Verify that the book is removed successfully
        self.assertNotIn("1984", self.driver.page_source)

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the Dashboard Page after logging out
        self.driver.get('http://localhost:8995/dashboard')
        time.sleep(1)  # Wait for the action to complete

        # Verify that access to the Dashboard is denied
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # Add a book to the reading list and then log out
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'query').send_keys('1984')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load
        self.driver.find_element(By.LINK_TEXT, '1984').click()
        time.sleep(1)  # Wait for the book details page to load
        self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()
        time.sleep(1)  # Wait for the action to complete
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Log back in with the same account
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8995/reading_list')
        time.sleep(1)  # Wait for the reading list page to load

        # Verify that the previously added book appears in the reading list
        self.assertIn("1984", self.driver.page_source)

        # Modify the reading list by adding and removing books
        self.driver.find_element(By.LINK_TEXT, 'Remove').click()
        time.sleep(1)  # Wait for the action to complete

        # Verify that the changes are reflected correctly
        self.assertNotIn("1984", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
