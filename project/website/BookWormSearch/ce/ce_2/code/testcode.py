import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestBookWormSearchApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8291/')  # Access the login page

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
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()

        # Enter a valid username and password
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        error_message = self.driver.find_element(By.XPATH, '//p[contains(text(), "Username already exists.")]')
        self.assertIsNotNone(error_message)

    def test_user_login(self):
        # Test valid login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Test invalid login
        self.driver.get('http://localhost:8291/')  # Go back to login page
        self.login("admin", "wrong_password")
        error_message = self.driver.find_element(By.XPATH, '//p[contains(text(), "Invalid username or password.")]')
        self.assertIsNotNone(error_message)

    def test_book_search(self):
        # Login first
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'query').send_keys("The Great Gatsby")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify search results
        results = self.driver.find_elements(By.XPATH, '//li')
        self.assertGreater(len(results), 0, "No results found for the search query.")

        # Test no results found
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys("Nonexistent Book")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        no_results_message = self.driver.find_element(By.XPATH, '//p[contains(text(), "No results found for")]')
        self.assertIsNotNone(no_results_message)

    def test_view_book_details(self):
        # Login first
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "The Great Gatsby").click()

        # Verify book details
        self.assertIn("The Great Gatsby", self.driver.title)
        description = self.driver.find_element(By.XPATH, '//p[contains(text(), "A story of the Jazz Age in the United States.")]')
        self.assertIsNotNone(description)

    def test_add_book_to_reading_list(self):
        # Login first
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "The Great Gatsby").click()
        self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()

        # Verify confirmation message
        message = self.driver.find_element(By.XPATH, '//p[contains(text(), "Book added to your reading list.")]')
        self.assertIsNotNone(message)

        # Navigate to Reading List Page
        self.driver.find_element(By.LINK_TEXT, 'My Reading List').click()
        reading_list_books = self.driver.find_elements(By.XPATH, '//li')
        self.assertGreater(len(reading_list_books), 0, "Reading list is empty.")

    def test_view_and_manage_reading_list(self):
        # Login first
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'My Reading List').click()

        # Remove a book from the reading list
        remove_button = self.driver.find_element(By.XPATH, '//form[contains(@action, "reading_list")]//button[text()="Remove"]')
        remove_button.click()

        # Verify confirmation message
        message = self.driver.find_element(By.XPATH, '//p[contains(text(), "Book removed from your reading list.")]')
        self.assertIsNotNone(message)

    def test_user_logout(self):
        # Login first
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the dashboard
        self.driver.get('http://localhost:8291/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
