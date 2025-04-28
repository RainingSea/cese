import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestAlbumSharingApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the actual port from main.py

    def tearDown(self):
        # Close the web driver session
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
        self.driver.get('http://localhost:5000/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:5000/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:5000/login')  # Navigate to Login Page
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Invalid login
        self.driver.get('http://localhost:5000/login')
        self.login("admin", "wrongpassword")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_create_album(self):
        # Functionality 3: Create and Upload Travel Albums
        self.login("user1", "user123")  # Login to create an album
        self.driver.get('http://localhost:5000/create_album')  # Navigate to Create Album Page
        self.assertIn("Create Album", self.driver.title)

        # Fill in album details and submit
        self.driver.find_element(By.NAME, 'album_name').send_keys("My Vacation Album")
        # Simulate image upload (assuming the input accepts file paths)
        self.driver.find_element(By.NAME, 'images').send_keys("path/to/image1.jpg")  # Update with actual path
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        time.sleep(1)

        # Verify album creation confirmation
        self.assertIn("Album created successfully", self.driver.page_source)

        # Attempt to create an album without filling required fields
        self.driver.get('http://localhost:5000/create_album')
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        time.sleep(1)

        # Verify error message for missing fields
        self.assertIn("All fields must be filled", self.driver.page_source)

    def test_explore_albums(self):
        # Functionality 6: Explore and View Albums Shared by Others
        self.driver.get('http://localhost:5000/explore')  # Navigate to Explore Page
        self.assertIn("Explore Albums", self.driver.title)

        # Verify albums are displayed
        albums = self.driver.find_elements(By.CLASS_NAME, 'album')
        self.assertGreater(len(albums), 0, "No albums found.")

    def test_logout(self):
        # Functionality 9: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
