import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestWishlistTrackerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8287/')  # Use the port specified in main.py

    def tearDown(self):
        # Close the web driver session and the Flask application
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
        self.driver.get('http://localhost:8287/register')  # Navigate to Registration Page
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

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8287/')  # Navigate to Login Page
        self.assertIn("Login", self.driver.title)

        self.login("admin", "admin123")  # Valid login
        self.assertIn("Dashboard", self.driver.title)

        # Invalid login attempt
        self.driver.get('http://localhost:8287/')  # Navigate to Login Page again
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("wrongpassword")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.title)  # Should still be on login page

    def test_view_wishlist(self):
        # Functionality 4: View Wishlist
        self.login("admin", "admin123")  # Login successfully
        self.assertIn("Dashboard", self.driver.title)

        # Verify that the wishlist is displayed
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No wishlist items found.")

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Login successfully
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_data_persistence(self):
        # Functionality 8: Data Persistence
        self.login("admin", "admin123")  # Login successfully
        # Here we would add an item to the wishlist (not implemented in the codebase)
        # For now, we will just check if the items persist after logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load
        self.login("admin", "admin123")  # Login again
        self.assertIn("Dashboard", self.driver.title)

        # Verify that the wishlist still contains items (not implemented in the codebase)
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No wishlist items found after relogin.")

if __name__ == '__main__':
    unittest.main()
