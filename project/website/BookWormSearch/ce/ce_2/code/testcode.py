import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestBookWormSearchApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8301/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8301/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8301/register')
        self.driver.find_element(By.NAME, 'username').send_keys("user1")  # Existing user
        self.driver.find_element(By.NAME, 'password').send_keys("some_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("user1", "user123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8301/')
        self.login("user1", "wrong_password")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_book_search(self):
        # Functionality 3: Book Search
        self.login("user1", "user123")  # Login successfully
        self.assertIn("Dashboard", self.driver.title)

        # Search for a valid book
        search_query = "1984"
        self.driver.find_element(By.NAME, 'query').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that the search results are displayed
        self.assertIn("1984", self.driver.page_source)

        # Search for a non-existing book
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys("Nonexistent Book")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify no results found message
        self.assertIn("No results found", self.driver.page_source)

    def test_view_book_details(self):
        # Functionality 4: View Book Details
        self.login("user1", "user123")  # Login successfully
        self.driver.find_element(By.NAME, 'query').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.driver.find_element(By.LINK_TEXT, "1984").click()  # Click on the book title

        # Verify that the book details page is displayed
        self.assertIn("1984", self.driver.title)
        self.assertIn("George Orwell", self.driver.page_source)

    def test_add_book_to_reading_list(self):
        # Functionality 5: Add Book to Reading List
        self.login("user1", "user123")  # Login successfully
        self.driver.find_element(By.NAME, 'query').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.driver.find_element(By.LINK_TEXT, "1984").click()  # Click on the book title
        self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()

        # Verify that the book is added to the reading list
        self.driver.get('http://localhost:8301/reading_list')
        self.assertIn("1984", self.driver.page_source)

    def test_view_reading_list(self):
        # Functionality 6: View and Manage Reading List
        self.login("user1", "user123")  # Login successfully
        self.driver.get('http://localhost:8301/reading_list')

        # Verify that the reading list is displayed
        self.assertIn("Your Reading List", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("user1", "user123")  # Login successfully
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_data_storage(self):
        # Functionality 8: Local Data Storage
        self.login("user1", "user123")  # Login successfully
        self.driver.get('http://localhost:8301/reading_list')

        # Verify that previously added books are still in the reading list
        self.assertIn("The Great Gatsby", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
