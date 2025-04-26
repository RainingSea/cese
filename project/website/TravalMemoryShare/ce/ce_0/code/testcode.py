import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelMemoryShareApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8258/')  # Access the login page

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
        self.driver.get('http://localhost:8258/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8258/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already exists!", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8258/')
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_create_album(self):
        # Functionality 3: Create and Upload Travel Albums
        self.login("admin", "admin123")  # Login first
        self.driver.get('http://localhost:8258/dashboard')  # Navigate to Dashboard

        # Verify that the user can see the option to create a new album
        self.assertIn("Create Album", self.driver.page_source)

        # Create a new album
        self.driver.find_element(By.NAME, 'title').send_keys("Vacation")
        self.driver.find_element(By.NAME, 'description').send_keys("Summer vacation photos")
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()

        # Verify that the album is created successfully
        self.assertIn("Album created successfully", self.driver.page_source)

        # Attempt to create an album without filling in required fields
        self.driver.find_element(By.NAME, 'title').clear()  # Clear title
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        self.assertIn("All fields must be filled", self.driver.page_source)

    def test_explore_albums(self):
        # Functionality 6: Explore and View Albums Shared by Others
        self.login("admin", "admin123")  # Login first
        self.driver.get('http://localhost:8258/explore')  # Navigate to Explore Page

        # Verify that albums are displayed
        self.assertGreater(len(self.driver.find_elements(By.CLASS_NAME, 'list-group-item')), 0, "No albums found.")

    def test_logout(self):
        # Functionality 9: User Logout
        self.login("admin", "admin123")  # Login first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click Logout
        self.assertIn("Login", self.driver.title)  # Verify redirection to Login Page

if __name__ == '__main__':
    unittest.main()
