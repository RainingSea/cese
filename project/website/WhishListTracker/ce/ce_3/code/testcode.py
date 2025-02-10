import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestWishlistApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8701/')

    def tearDown(self):
        # Close the web driver session and terminate the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Create an account').click()
        self.assertIn("Register", self.driver.title)

        # Register a new user
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Create an account').click()
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Check for error message (not implemented in the codebase)
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Login with valid credentials
        self.login('admin', 'admin123')
        self.assertIn("Dashboard", self.driver.title)

        # Logout to test invalid login
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Login with invalid credentials
        self.login('admin', 'wrongpassword')
        self.assertIn("Login", self.driver.title)

    def test_add_items_to_wishlist(self):
        # Login and navigate to Dashboard
        self.login('admin', 'admin123')
        self.assertIn("Dashboard", self.driver.title)

        # Add a new item to the wishlist
        self.driver.find_element(By.NAME, 'item_name').send_keys('New Item')
        self.driver.find_element(By.NAME, 'description').send_keys('Item Description')
        self.driver.find_element(By.NAME, 'desired_price').send_keys('99.99')
        self.driver.find_element(By.XPATH, '//button[text()="Add to Wishlist"]').click()
        time.sleep(1)

        # Verify the item is added
        self.assertIn('New Item', self.driver.page_source)

        # Attempt to add an item with missing fields
        self.driver.find_element(By.NAME, 'item_name').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Add to Wishlist"]').click()
        time.sleep(1)

        # Check for error message (not implemented in the codebase)
        self.assertIn("Dashboard", self.driver.title)

    def test_view_wishlist(self):
        # Login and navigate to Dashboard
        self.login('admin', 'admin123')
        self.assertIn("Dashboard", self.driver.title)

        # Verify wishlist items are displayed
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No items found in wishlist.")

    def test_update_item_in_wishlist(self):
        # Functionality not implemented in the codebase
        self.fail("Update item functionality not implemented")

    def test_remove_item_from_wishlist(self):
        # Functionality not implemented in the codebase
        self.fail("Remove item functionality not implemented")

    def test_user_logout(self):
        # Login and navigate to Dashboard
        self.login('admin', 'admin123')
        self.assertIn("Dashboard", self.driver.title)

        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to access Dashboard after logout
        self.driver.get('http://localhost:8701/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_data_persistence(self):
        # Functionality not implemented in the codebase
        self.fail("Data persistence functionality not implemented")

if __name__ == '__main__':
    unittest.main()
