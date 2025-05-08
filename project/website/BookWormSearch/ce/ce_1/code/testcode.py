import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestBookWormSearchApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8290/')  # Access the application on the assigned port

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
        self.driver.get('http://localhost:8290/registration')
        
        # Enter valid username and password
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Check for success message
        self.assertIn("Registration successful", self.driver.page_source)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8290/registration')
        self.driver.find_element(By.NAME, 'username').send_keys('admin')  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Check for error message
        self.assertIn("Username already exists", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8290/login')

        # Enter valid credentials
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8290/login')
        self.login("invalid_user", "wrong_password")
        self.assertIn("Invalid username or password", self.driver.page_source)

    def test_book_search(self):
        # Functionality 3: Book Search
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8290/dashboard')

        # Search for a book
        search_box = self.driver.find_element(By.NAME, 'query')
        search_box.send_keys("1984")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Check for search results
        self.assertIn("1984", self.driver.page_source)

        # Search for a non-existing book
        search_box.clear()
        search_box.send_keys("Nonexistent Book")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.assertIn("No books found", self.driver.page_source)

    def test_view_book_details(self):
        # Functionality 4: View Book Details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8290/dashboard')
        self.driver.find_element(By.LINK_TEXT, "1984").click()

        # Check if book details are displayed
        self.assertIn("1984", self.driver.page_source)
        self.assertIn("George Orwell", self.driver.page_source)

    def test_add_book_to_reading_list(self):
        # Functionality 5: Add Book to Reading List
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8290/book/1984')
        self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()

        # Check for confirmation message
        self.assertIn('"1984" added to your reading list.', self.driver.page_source)

        # Navigate to Reading List
        self.driver.get('http://localhost:8290/reading_list')
        self.assertIn("1984", self.driver.page_source)

    def test_view_and_manage_reading_list(self):
        # Functionality 6: View and Manage Reading List
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8290/reading_list')

        # Check if reading list is displayed
        self.assertIn("The Great Gatsby", self.driver.page_source)

        # Remove a book from the reading list
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        self.assertNotIn("The Great Gatsby", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # Functionality 8: Local Data Storage
        self.login("user1", "user123")
        self.driver.get('http://localhost:8290/reading_list')

        # Check if the reading list is populated
        self.assertIn("1984", self.driver.page_source)

        # Add and remove books to check data integrity
        self.driver.get('http://localhost:8290/book/The Great Gatsby')
        self.driver.find_element(By.XPATH, '//button[text()="Add to Reading List"]').click()
        self.driver.get('http://localhost:8290/reading_list')
        self.assertIn("The Great Gatsby", self.driver.page_source)

        # Remove the book
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        self.assertNotIn("The Great Gatsby", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
