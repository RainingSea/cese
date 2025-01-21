import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestBookWormSearch(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start

        # Initialize the webdriver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8996/')

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
        time.sleep(1)

        # Verify Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter valid username and password
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("Register", self.driver.title)  # Assuming the page stays the same

    def test_user_login(self):
        # Verify Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("admin", "admin123")

        # Verify redirection to Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8996/')
        self.login("invalid_user", "invalid_pass")

        # Verify error message for invalid credentials
        self.assertIn("Login", self.driver.title)  # Assuming the page stays the same

    def test_book_search(self):
        self.login("admin", "admin123")

        # Verify Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Search for a valid book title
        # Assuming a search bar and button exist
        # self.driver.find_element(By.NAME, 'search').send_keys("The Great Gatsby")
        # self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        # time.sleep(1)

        # Verify search results
        # self.assertIn("The Great Gatsby", self.driver.page_source)

        # Search for a non-existing book
        # self.driver.find_element(By.NAME, 'search').clear()
        # self.driver.find_element(By.NAME, 'search').send_keys("Non Existing Book")
        # self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        # time.sleep(1)

        # Verify no results message
        # self.assertIn("No results found", self.driver.page_source)

        self.fail("Book search functionality not implemented")

    def test_view_book_details(self):
        self.login("admin", "admin123")

        # Click on a book link
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)

        # Verify Book Details Page
        self.assertIn("The Great Gatsby", self.driver.title)
        self.assertIn("F. Scott Fitzgerald", self.driver.page_source)
        self.assertIn("A novel set in the 1920s about the mysterious Jay Gatsby.", self.driver.page_source)

    def test_add_book_to_reading_list(self):
        self.login("admin", "admin123")

        # Navigate to Book Details Page
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)

        # Click "Add to Reading List"
        # Assuming a button exists
        # self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()
        # time.sleep(1)

        # Verify confirmation message
        # self.assertIn("added to your reading list", self.driver.page_source)

        # Navigate to Reading List Page
        self.driver.find_element(By.LINK_TEXT, 'My Reading List').click()
        time.sleep(1)

        # Verify book appears in the reading list
        # self.assertIn("The Great Gatsby", self.driver.page_source)

        self.fail("Add to reading list functionality not implemented")

    def test_view_and_manage_reading_list(self):
        self.login("admin", "admin123")

        # Navigate to Reading List Page
        self.driver.find_element(By.LINK_TEXT, 'My Reading List').click()
        time.sleep(1)

        # Verify Reading List Page
        self.assertIn("My Reading List", self.driver.title)

        # Remove a book from the reading list
        # Assuming a remove button exists
        # self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        # time.sleep(1)

        # Verify book is removed
        # self.assertNotIn("The Great Gatsby", self.driver.page_source)

        self.fail("Manage reading list functionality not implemented")

    def test_user_logout(self):
        self.login("admin", "admin123")

        # Click Logout
        # Assuming a logout link or button exists
        # self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        # time.sleep(1)

        # Verify redirection to Login Page
        # self.assertIn("Login", self.driver.title)

        # Attempt to access Dashboard
        # self.driver.get('http://localhost:8996/dashboard')
        # self.assertIn("Login", self.driver.title)

        self.fail("Logout functionality not implemented")

    def test_local_data_storage(self):
        self.login("admin", "admin123")

        # Add a book to the reading list
        # Assuming a method to add exists
        # self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        # self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()
        # time.sleep(1)

        # Logout and login again
        # self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        # time.sleep(1)
        # self.login("admin", "admin123")

        # Verify book is still in the reading list
        # self.driver.find_element(By.LINK_TEXT, 'My Reading List').click()
        # time.sleep(1)
        # self.assertIn("The Great Gatsby", self.driver.page_source)

        self.fail("Local data storage functionality not implemented")

if __name__ == '__main__':
    unittest.main()
