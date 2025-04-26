import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestWebApplication(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8227/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the application process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8227/register')  # Navigate to Registration Page
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
        self.driver.get('http://localhost:8227/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8227/')
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_search_books(self):
        # Functionality 3: Search for Specific Words or Phrases
        self.login("admin", "admin123")  # Login to access dashboard
        self.assertIn("Dashboard", self.driver.title)

        # Search for a specific book
        search_query = "1984"
        self.driver.find_element(By.NAME, 'query').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify search results
        self.assertIn("1984", self.driver.page_source)

        # Search for a non-existing book
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys("Nonexistent Book")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.assertIn("No results found", self.driver.page_source)

    def test_view_book_details(self):
        # Functionality 4: View Book Details
        self.login("admin", "admin123")  # Login to access dashboard
        self.driver.find_element(By.LINK_TEXT, "1984").click()  # Click on the book link
        self.assertIn("1984", self.driver.title)
        self.assertIn("George Orwell", self.driver.page_source)

    def test_add_to_reading_list(self):
        # Functionality 5: Add Books to Reading List
        self.login("admin", "admin123")  # Login to access dashboard
        self.driver.find_element(By.LINK_TEXT, "1984").click()  # Click on the book link
        self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()
        self.assertIn("Book added to reading list", self.driver.page_source)

    def test_view_reading_list(self):
        # Functionality 6: View and Manage Reading List
        self.login("admin", "admin123")  # Login to access dashboard
        self.driver.get('http://localhost:8227/reading_list')  # Navigate to Reading List Page
        self.assertIn("Your Reading List", self.driver.title)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Login to access dashboard
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 8: Navigate Back to Dashboard
        self.login("admin", "admin123")  # Login to access dashboard
        self.driver.find_element(By.LINK_TEXT, "1984").click()  # Click on the book link
        self.driver.find_element(By.LINK_TEXT, "Back to Dashboard").click()
        self.assertIn("Dashboard", self.driver.title)

    def test_view_detailed_information(self):
        # Functionality 9: View Detailed Information
        self.login("admin", "admin123")  # Login to access dashboard
        self.driver.find_element(By.LINK_TEXT, "1984").click()  # Click on the book link
        self.assertIn("1984", self.driver.page_source)
        self.assertIn("A dystopian novel about totalitarianism.", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
