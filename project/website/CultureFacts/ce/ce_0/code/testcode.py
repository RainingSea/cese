import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCultureFactsApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8311/')  # Use the port from main.py

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
        self.driver.get('http://localhost:8311/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8311/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify that an error message is displayed
        self.assertIn("already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8311/')  # Navigate to Login Page
        self.assertIn("Login", self.driver.title)

        self.login("admin", "admin123")  # Valid credentials

        # Verify that the Dashboard Page has loaded
        self.assertIn("Culture Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8311/')
        self.login("admin", "wrong_password")

        # Verify that an error message is displayed
        self.assertIn("incorrect", self.driver.page_source)

    def test_explore_cultures(self):
        # Functionality 3: Explore Cultures on the Dashboard Page
        self.login("admin", "admin123")  # Login first
        self.assertIn("Culture Dashboard", self.driver.title)

        # Verify that a list of cultures is displayed
        cultures = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cultures), 0, "No cultures found on the dashboard.")

        # Click on a culture
        cultures[0].click()  # Click the first culture
        self.assertIn("Culture Details", self.driver.title)

    def test_view_culture_details(self):
        # Functionality 4: View Culture Details
        self.login("admin", "admin123")  # Login first
        self.driver.get('http://localhost:8311/dashboard')
        culture_link = self.driver.find_element(By.LINK_TEXT, "Japanese")
        culture_link.click()

        # Verify that the Culture Details Page is displayed
        self.assertIn("Japanese", self.driver.title)
        self.assertIn("Japan is an island country", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")  # Login first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8311/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
