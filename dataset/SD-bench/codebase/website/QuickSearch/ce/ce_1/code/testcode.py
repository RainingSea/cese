import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestQuickSearchApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8681/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and stop the application
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

        # Verify the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
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

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)  # Assuming it stays on the registration page

    def test_user_login(self):
        # Verify the Login form is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8681/')  # Navigate back to the login page
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)  # Assuming it stays on the login page

    def test_search_for_specific_words_or_phrases(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Enter a specific word or phrase in the search bar and submit
        self.driver.find_element(By.NAME, 'query').send_keys("Gatsby")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results

        # Verify a list of matching results is displayed
        results = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(results), 0, "No search results found.")

        # Enter a word or phrase that does not exist in the collection
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys("NonExistentBook")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results

        # Verify a message is displayed indicating no results were found
        results = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(results), 0, "Unexpected search results found.")

    def test_view_book_details(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Click on a book from the search results
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)  # Wait for the book details page

        # Verify the Book Details Page is displayed
        self.assertIn("The Great Gatsby", self.driver.title)

    def test_add_books_to_reading_list(self):
        # Navigate to the Book Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)  # Wait for the book details page

        # Click the 'Add to Reading List' button
        self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()
        time.sleep(1)  # Wait for the action to complete

        # Navigate to the Reading List Page
        self.driver.find_element(By.LINK_TEXT, 'My Reading List').click()
        time.sleep(1)  # Wait for the reading list page

        # Verify the added book appears in the reading list
        reading_list_books = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(reading_list_books), 0, "No books found in the reading list.")

    def test_view_and_manage_reading_list(self):
        # Login and navigate to the Reading List Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'My Reading List').click()
        time.sleep(1)  # Wait for the reading list page

        # Verify the user's reading list is displayed
        reading_list_books = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(reading_list_books), 0, "No books found in the reading list.")

        # Remove a book from the reading list (not implemented in the codebase)
        self.fail("Remove book from reading list functionality not implemented")

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Logout from the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the login page

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Navigate to the Book Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)  # Wait for the book details page

        # Click the back button to return to the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)  # Wait for the dashboard page

        # Verify the user is redirected back to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

    def test_view_detailed_information(self):
        # Click the 'Details' button for a specific book on the Dashboard Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'The Great Gatsby').click()
        time.sleep(1)  # Wait for the book details page

        # Verify the detailed information for that book is displayed
        self.assertIn("The Great Gatsby", self.driver.title)
        self.assertIn("F. Scott Fitzgerald", self.driver.page_source)
        self.assertIn("A novel about the American dream.", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
