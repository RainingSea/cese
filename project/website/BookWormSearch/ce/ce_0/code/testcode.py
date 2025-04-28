import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestBookWormSearchApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8299/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:8299/login')
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8299/register')
        
        # Verify that the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8299/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify that an error message is displayed
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8299/login')
        self.driver.find_element(By.NAME, 'username').send_keys("invalid_user")
        self.driver.find_element(By.NAME, 'password').send_keys("invalid_password")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

        # Verify that an error message is displayed
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_book_search(self):
        # Functionality 3: Book Search
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8299/dashboard')

        # Verify that the Dashboard Page is displayed with a search bar
        self.assertIn("Dashboard", self.driver.title)

        # Search for a valid book title
        self.driver.find_element(By.NAME, 'query').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that the search results are displayed
        self.assertIn("1984", self.driver.page_source)

        # Search for a non-existing book
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys("Nonexistent Book")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that no results are found
        self.assertIn("No results found", self.driver.page_source)

    def test_view_book_details(self):
        # Functionality 4: View Book Details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8299/dashboard')
        self.driver.find_element(By.LINK_TEXT, "1984").click()

        # Verify that the Book Details Page is displayed
        self.assertIn("Book Details", self.driver.title)
        self.assertIn("George Orwell", self.driver.page_source)
        self.assertIn("A dystopian novel set in a totalitarian society ruled by Big Brother.", self.driver.page_source)

    def test_add_book_to_reading_list(self):
        # Functionality 5: Add Book to Reading List
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8299/book/1984')
        self.driver.find_element(By.LINK_TEXT, "Add to Reading List").click()

        # Verify that the book is added to the reading list
        self.driver.get('http://localhost:8299/reading_list')
        self.assertIn("1984", self.driver.page_source)

    def test_view_reading_list(self):
        # Functionality 6: View and Manage Reading List
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8299/reading_list')

        # Verify that the Reading List Page displays the user's current reading list
        self.assertIn("The Great Gatsby", self.driver.page_source)
        self.assertIn("1984", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Logout").click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_data_storage(self):
        # Functionality 8: Local Data Storage
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8299/book/The Great Gatsby')
        self.driver.find_element(By.LINK_TEXT, "Add to Reading List").click()
        self.driver.find_element(By.LINK_TEXT, "Logout").click()

        # Log back in
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8299/reading_list')

        # Verify that the previously added book appears in the reading list
        self.assertIn("The Great Gatsby", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
