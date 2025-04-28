import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestBookApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8398/')  # Use the port from main.py

    def tearDown(self):
        # Close the web driver session and terminate the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        # Enter a valid username and password
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify that an error message is displayed
        self.assertIn("Username already taken", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8398/')  # Ensure we are on the login page

        # Enter valid credentials
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8398/')  # Go back to login page
        self.login("admin", "wrongpassword")

        # Verify that an error message is displayed
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_search_books(self):
        # Login successfully
        self.login("admin", "admin123")

        # Verify that the search bar is displayed
        self.assertTrue(self.driver.find_element(By.NAME, 'search'))

        # Enter a search query
        search_query = "1984"
        self.driver.find_element(By.NAME, 'search').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that the search results are displayed
        self.assertIn("1984", self.driver.page_source)

        # Search for a non-existing book
        self.driver.find_element(By.NAME, 'search').clear()
        self.driver.find_element(By.NAME, 'search').send_keys("NonExistingBook")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that no results message is displayed
        self.assertIn("No results found", self.driver.page_source)

    def test_view_book_details(self):
        # Login successfully
        self.login("admin", "admin123")

        # Search for a book
        self.driver.find_element(By.NAME, 'search').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Click on the book title to view details
        self.driver.find_element(By.LINK_TEXT, "1984").click()

        # Verify that the book details are displayed
        self.assertIn("1984", self.driver.page_source)
        self.assertIn("George Orwell", self.driver.page_source)

    def test_add_to_reading_list(self):
        # Login successfully
        self.login("admin", "admin123")

        # Search for a book
        self.driver.find_element(By.NAME, 'search').send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Click on the book title to view details
        self.driver.find_element(By.LINK_TEXT, "1984").click()

        # Add the book to the reading list
        self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()

        # Verify that the book has been added to the reading list
        self.driver.get('http://localhost:8398/reading_list')
        self.assertIn("1984", self.driver.page_source)

    def test_logout(self):
        # Login successfully
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8398/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
