import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTravelMemoryShareApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8260/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8260/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)  # Check if Registration Page is displayed

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify registration success
        self.assertIn("Login", self.driver.title)  # Check if redirected to Login Page

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8260/register')  # Navigate to Registration Page
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8260/')  # Navigate to Login Page
        self.assertIn("Login", self.driver.title)  # Check if Login Page is displayed

        # Successful login
        self.login("admin", "admin123")
        self.assertIn("Explore", self.driver.title)  # Check if redirected to Explore Page

        # Invalid login attempt
        self.driver.get('http://localhost:8260/')  # Navigate to Login Page
        self.login("admin", "wrongpassword")
        self.assertIn("Invalid credentials", self.driver.page_source)  # Check for error message

    def test_create_album(self):
        # Functionality 3: Create and Upload Travel Albums
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8260/album/create')  # Navigate to Create Album Page
        self.assertIn("Create Album", self.driver.title)  # Check if Create Album Page is displayed

        # Create a new album
        self.driver.find_element(By.NAME, 'title').send_keys("Summer Vacation")
        self.driver.find_element(By.NAME, 'description').send_keys("A trip to the beach")
        self.driver.find_element(By.NAME, 'images').send_keys("image1.jpg,image2.jpg")
        self.driver.find_element(By.NAME, 'visibility').send_keys("public")
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify album creation success
        self.assertIn("Album created successfully!", self.driver.page_source)

        # Attempt to create an album without filling required fields
        self.driver.get('http://localhost:8260/album/create')  # Navigate to Create Album Page
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()  # Submit empty form
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for missing fields
        self.assertIn("All fields must be filled", self.driver.page_source)

    def test_explore_albums(self):
        # Functionality 6: Explore and View Albums Shared by Others
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8260/explore')  # Navigate to Explore Page
        self.assertIn("Explore Albums", self.driver.title)  # Check if Explore Page is displayed

        # Verify that albums are displayed
        self.assertIn("Summer Vacation", self.driver.page_source)  # Check for the album title

    def test_logout(self):
        # Functionality 9: User Logout
        self.login("admin", "admin123")  # Log in first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click Logout
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
