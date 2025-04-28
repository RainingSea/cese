import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelMemoryShareApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8430/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8430/')  # Navigate to the Registration Page

        # Enter a valid username and password, then click the "Register" button
        self.driver.find_element(By.ID, 'new_username').send_keys("new_user")
        self.driver.find_element(By.ID, 'new_password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Expectation: The user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.get('http://localhost:8430/')  # Navigate to the Registration Page again
        self.driver.find_element(By.ID, 'new_username').send_keys("admin")  # Existing username
        self.driver.find_element(By.ID, 'new_password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Expectation: An error message is displayed
        self.assertIn("Registration failed", self.driver.page_source)

    def test_user_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8430/')  # Navigate to the Login Page

        # Enter valid credentials
        self.login("admin", "admin123")

        # Expectation: Access is granted, and the user is redirected to the Dashboard Page
        self.assertIn("Explore Albums", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8430/')  # Navigate to the Login Page again
        self.login("admin", "wrongpassword")

        # Expectation: An error message is displayed
        self.assertIn("Login failed", self.driver.page_source)

    def test_create_album(self):
        # Functionality 3: Create and Upload Travel Albums
        self.login("admin", "admin123")  # Login successfully

        # Navigate to album creation page (assuming a link exists)
        self.driver.get('http://localhost:8430/album_creation')  # Replace with actual URL if needed

        # Fill in the album details
        self.driver.find_element(By.NAME, 'title').send_keys("My Summer Vacation")
        self.driver.find_element(By.NAME, 'images').send_keys("image1.jpg,image2.jpg,image3.jpg")
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()

        # Expectation: The album is created successfully
        self.assertIn("Album created successfully", self.driver.page_source)

        # Attempt to create an album without filling in required fields
        self.driver.get('http://localhost:8430/album_creation')  # Navigate to album creation page again
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()

        # Expectation: An error message is displayed
        self.assertIn("All required fields must be filled", self.driver.page_source)

    def test_explore_albums(self):
        # Functionality 6: Explore and View Albums Shared by Others
        self.login("admin", "admin123")  # Login successfully

        # Navigate to the album exploration page
        self.driver.get('http://localhost:8430/album_exploration')

        # Expectation: A list of albums shared by other users is displayed
        albums = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(albums), 0, "No albums found.")

    def test_logout(self):
        # Functionality 9: User Logout
        self.login("admin", "admin123")  # Login successfully

        # Click the Logout button (assuming it exists)
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Expectation: The user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
