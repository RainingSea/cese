import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCultureFactsApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8148/')  # Use the port from main.py

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:8148/')  # Navigate to login page
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8148/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8148/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Check for error message
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Culture Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8148/')
        self.login("admin", "wrongpassword")
        
        # Check for error message
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_explore_cultures(self):
        # Functionality 3: Explore Cultures on the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Culture Dashboard", self.driver.title)

        # Click on a culture from the list
        self.driver.find_element(By.LINK_TEXT, "Japanese").click()

        # Verify that the Culture Details Page has loaded
        self.assertIn("Japanese Details", self.driver.title)

    def test_view_culture_details(self):
        # Functionality 4: View Culture Details
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Japanese").click()

        # Check if the details are present
        self.assertIn("Rich history", self.driver.page_source)
        self.assertIn("Unique traditions", self.driver.page_source)
        self.assertIn("Delicious cuisine", self.driver.page_source)

    def test_bookmark_culture(self):
        # Functionality 6: Bookmark Culture Facts
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Japanese").click()
        self.driver.find_element(By.XPATH, '//a[text()="Bookmark"]').click()

        # Verify that the culture is bookmarked
        self.driver.get('http://localhost:8148/bookmarks')
        self.assertIn("Japanese", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8148/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
