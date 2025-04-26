import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestBookManagementApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8226/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.get('http://localhost:8226/register')
        
        # Verify the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "testuser"
        new_password = "testpass"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8226/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8226/')
        
        # Verify the Login form is displayed
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("admin", "admin123")

        # Verify redirection to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8226/')
        self.login("admin", "wrongpassword")

        # Verify error message for incorrect credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_search_books(self):
        # Login first
        self.login("admin", "admin123")
        
        # Navigate to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Search for a specific book
        search_query = "1984"
        self.driver.find_element(By.NAME, 'query').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that search results are displayed
        self.assertIn("1984", self.driver.page_source)

        # Search for a non-existing book
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys("Nonexistent Book")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify no results found message
        self.assertIn("No results found", self.driver.page_source)

    def test_view_book_details(self):
        # Login first
        self.login("admin", "admin123")
        
        # Navigate to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Click on a book from the search results
        self.driver.find_element(By.LINK_TEXT, "1984").click()

        # Verify that the Book Details Page is displayed
        self.assertIn("1984", self.driver.title)
        self.assertIn("A dystopian novel about totalitarianism and surveillance.", self.driver.page_source)

    def test_add_to_reading_list(self):
        # Login first
        self.login("admin", "admin123")
        
        # Navigate to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Click on a book to view details
        self.driver.find_element(By.LINK_TEXT, "1984").click()

        # Add the book to the reading list
        self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()

        # Verify that the book is added to the reading list
        self.driver.get('http://localhost:8226/reading_list')
        self.assertIn("1984", self.driver.page_source)

    def test_view_reading_list(self):
        # Login first
        self.login("admin", "admin123")
        
        # Navigate to the Reading List Page
        self.driver.get('http://localhost:8226/reading_list')

        # Verify that the reading list is displayed
        self.assertIn("My Reading List", self.driver.page_source)

    def test_logout(self):
        # Login first
        self.login("admin", "admin123")
        
        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
