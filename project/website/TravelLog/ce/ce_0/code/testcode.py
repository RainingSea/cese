import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelLogApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8438/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8438/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)  # Check if registration form is displayed

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8438/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Check for error message
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Entries Overview", self.driver.title)  # Check if redirected to overview page

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8438/')
        self.login("admin", "wrong_password")
        self.assertIn("Invalid credentials", self.driver.page_source)  # Check for error message

    def test_create_journal_entry(self):
        # Functionality 3: Create and Save Travel Journal Entries
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8438/journal')  # Navigate to journal entry page
        self.assertIn("Create Journal Entry", self.driver.title)  # Check if form is displayed

        # Fill in the journal entry form
        self.driver.find_element(By.NAME, 'destination').send_keys("Paris")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-05-01")
        self.driver.find_element(By.NAME, 'activities').send_keys("Visited Eiffel Tower")
        self.driver.find_element(By.NAME, 'photos').send_keys("path/to/photo1.jpg")  # Adjust path as necessary
        self.driver.find_element(By.NAME, 'reflections').send_keys("It was amazing!")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify entry is saved and displayed on overview page
        self.driver.get('http://localhost:8438/overview')
        self.assertIn("Paris", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")  # Log in first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click logout
        self.assertIn("Login", self.driver.title)  # Check if redirected to login page

    def test_navigate_back_to_dashboard(self):
        # Functionality 9: Navigate Back to Dashboard
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8438/journal')  # Navigate to journal entry page
        self.driver.find_element(By.LINK_TEXT, 'Back to Overview').click()  # Click back to overview
        self.assertIn("Entries Overview", self.driver.title)  # Check if redirected to overview page

if __name__ == '__main__':
    unittest.main()
