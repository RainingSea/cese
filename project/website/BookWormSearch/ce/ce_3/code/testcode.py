import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestBookWormSearch(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Allow some time for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8590/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and stop the web application
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
        new_username = "test_user"
        new_password = "test_password"
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

        # Verify that an error message is displayed
        self.assertIn("Register", self.driver.title)  # Assuming it stays on the same page

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8590/')  # Navigate back to login
        self.login("invalid_user", "invalid_pass")

        # Verify that an error message is displayed
        self.assertIn("Login", self.driver.title)  # Assuming it stays on the login page

    def test_book_search(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Enter a valid book title in the search bar and click the "Search" button
        self.driver.find_element(By.NAME, 'search').send_keys("Sample Book")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the results to load

        # Verify that a list of matching book results is displayed
        self.assertIn("Sample Book", self.driver.page_source)

        # Enter a keyword that does not match any book titles or authors
        self.driver.find_element(By.NAME, 'search').clear()
        self.driver.find_element(By.NAME, 'search').send_keys("Nonexistent Book")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the results to load

        # Verify that a message is displayed indicating no results were found
        self.assertNotIn("Nonexistent Book", self.driver.page_source)

    def test_view_book_details(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Click on a book from the search results
        self.driver.find_element(By.LINK_TEXT, 'Sample Book').click()
        time.sleep(1)  # Wait for the Book Details Page to load

        # Verify that the Book Details Page is displayed with detailed information
        self.assertIn("Sample Book", self.driver.title)
        self.assertIn("Sample Author", self.driver.page_source)
        self.assertIn("Sample Summary", self.driver.page_source)

    def test_add_book_to_reading_list(self):
        # This functionality is not implemented in the codebase
        self.fail("Add to Reading List functionality not implemented")

    def test_view_and_manage_reading_list(self):
        # Login successfully and navigate to the Reading List Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'My Reading List').click()
        time.sleep(1)  # Wait for the Reading List Page to load

        # Verify that the Reading List Page displays the user's current reading list
        self.assertIn("My Reading List", self.driver.title)

        # Remove a book from the reading list
        # This functionality is not implemented in the codebase
        self.fail("Remove book from Reading List functionality not implemented")

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Logout from the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the Login Page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the Dashboard Page after logging out
        self.driver.get('http://localhost:8590/dashboard')
        self.assertIn("Login", self.driver.title)  # Should redirect to login

    def test_local_data_storage(self):
        # This functionality is not implemented in the codebase
        self.fail("Local Data Storage functionality not implemented")

if __name__ == '__main__':
    unittest.main()
