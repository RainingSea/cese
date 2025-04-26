import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelMemoryShareApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8259/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8259/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify registration success
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8259/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already exists", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Album Creation", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8259/')
        self.login("admin", "wrongpassword")
        self.assertIn("Invalid username or password", self.driver.page_source)

    def test_create_album(self):
        # Functionality 3: Create and Upload Travel Albums
        self.login("admin", "admin123")  # Login first
        self.driver.get('http://localhost:8259/album_creation')  # Navigate to Album Creation Page
        self.assertIn("Create Album", self.driver.title)

        # Create an album
        self.driver.find_element(By.NAME, 'title').send_keys("My Travel Album")
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        self.assertIn("Album created successfully!", self.driver.page_source)

        # Attempt to create an album without filling in required fields
        self.driver.get('http://localhost:8259/album_creation')
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        self.assertIn("All required fields must be filled", self.driver.page_source)

    def test_logout(self):
        # Functionality 9: User Logout
        self.login("admin", "admin123")  # Login first
        self.driver.get('http://localhost:8259/')  # Navigate to login page
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8259/album_creation')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
