import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestBookManagementApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8399/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.driver.find_element(By.NAME, 'username').send_keys("user1")  # Existing user
        self.driver.find_element(By.NAME, 'password').send_keys("password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already exists.", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("user1", "user123")
        
        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.login("user1", "wrongpassword")
        
        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials.", self.driver.page_source)

    def test_search_books(self):
        # Functionality 3: Search for Specific Words or Phrases
        self.login("user1", "user123")
        
        # Verify that the search bar is displayed
        self.assertIn("Search for books...", self.driver.page_source)

        # Search for a book that exists
        self.driver.find_element(By.NAME, 'query').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that search results are displayed
        self.assertIn("1984", self.driver.page_source)

        # Search for a book that does not exist
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys("Nonexistent Book")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify no results found message
        self.assertIn("No results found.", self.driver.page_source)

    def test_view_book_details(self):
        # Functionality 4: View Book Details
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, "1984").click()  # Click on the book link

        # Verify that the Book Details Page is displayed
        self.assertIn("1984", self.driver.title)
        self.assertIn("George Orwell", self.driver.page_source)

    def test_add_to_reading_list(self):
        # Functionality 5: Add Books to Reading List
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, "1984").click()  # Click on the book link
        self.driver.find_element(By.LINK_TEXT, "Add to Reading List").click()

        # Verify that the book is added to the reading list
        self.driver.get('http://localhost:8399/reading_list')
        self.assertIn("1984", self.driver.page_source)

    def test_view_reading_list(self):
        # Functionality 6: View and Manage Reading List
        self.login("user1", "user123")
        self.driver.get('http://localhost:8399/reading_list')

        # Verify that the reading list is displayed
        self.assertIn("Your Reading List", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 8: Navigate Back to Dashboard
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, "1984").click()  # Click on the book link
        self.driver.find_element(By.LINK_TEXT, "Back to Dashboard").click()

        # Verify that the user is redirected back to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

    def test_view_detailed_information(self):
        # Functionality 9: View Detailed Information
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, "1984").click()  # Click on the book link

        # Verify that the detailed information for the book is displayed
        self.assertIn("A dystopian novel about totalitarianism.", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
