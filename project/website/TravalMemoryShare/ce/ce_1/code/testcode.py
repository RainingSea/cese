import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelMemoryShareApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8431/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8431/register')
        
        # Verify that the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8431/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8431/')
        
        # Verify that the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Invalid login
        self.driver.get('http://localhost:8431/')
        self.login("admin", "wrongpassword")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_create_album(self):
        # Functionality 3: Create and Upload Travel Albums
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8431/album/create')

        # Verify that the Create Album Page is displayed
        self.assertIn("Create Album", self.driver.title)

        # Fill in album details
        self.driver.find_element(By.NAME, 'title').send_keys("Summer Vacation")
        self.driver.find_element(By.NAME, 'images').send_keys("beach.jpg,mountains.jpg")
        self.driver.find_element(By.NAME, 'privacy').send_keys("public")
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()

        # Verify album creation
        self.assertIn("Album created successfully", self.driver.page_source)

        # Attempt to create an album without filling required fields
        self.driver.get('http://localhost:8431/album/create')
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        self.assertIn("All fields must be filled", self.driver.page_source)

    def test_logout(self):
        # Functionality 9: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8431/')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
