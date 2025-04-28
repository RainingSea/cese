import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestShopPalApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8412/')  # Access the login page

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
        self.driver.get('http://localhost:8412/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)  # Check if Registration form is displayed

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
        self.driver.get('http://localhost:8412/register')  # Navigate to Registration Page
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check for error message
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8412/')  # Navigate back to login page
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("wrongpassword")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check for error message
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_view_product_details(self):
        # Functionality 5: View Detailed Product Information
        self.login("admin", "admin123")  # Log in first

        # Navigate to a product detail page
        self.driver.get('http://localhost:8412/product/001')  # Access product with ID 001
        time.sleep(1)  # Wait for the next page to load

        # Verify that the product details are displayed
        self.assertIn("Product A details", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Log in first

        # Click the Logout link
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 8: Navigate Back to Dashboard
        self.login("admin", "admin123")  # Log in first

        # Navigate to a product detail page
        self.driver.get('http://localhost:8412/product/001')  # Access product with ID 001
        time.sleep(1)  # Wait for the next page to load

        # Click the back button to return to the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.title)

if __name__ == '__main__':
    unittest.main()
