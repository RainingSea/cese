import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestWishlistTracker(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8699/')  # Navigate to the login page

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

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register here.").click()
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register here.").click()
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check for error message
        self.assertIn("Registration", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8699/')  # Navigate back to login page
        self.login("invalid_user", "invalid_password")
        self.assertIn("Login", self.driver.title)

    def test_add_items_to_wishlist(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Enter item name, description, and price, then submit the form
        self.driver.find_element(By.NAME, 'item_name').send_keys('New Item')
        self.driver.find_element(By.NAME, 'description').send_keys('A new item description')
        self.driver.find_element(By.NAME, 'price').send_keys('10.99')
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        time.sleep(1)  # Wait for the item to be added

        # Verify the item is added to the wishlist
        self.assertIn("New Item", self.driver.page_source)

    def test_view_wishlist(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Verify the wishlist is displayed
        wishlist_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(wishlist_items), 0, "No items found in the wishlist.")

    def test_update_item_in_wishlist(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Update an item in the wishlist
        self.driver.find_element(By.NAME, 'old_item_name').send_keys('item1')
        self.driver.find_element(By.NAME, 'new_item_name').send_keys('Updated Item')
        self.driver.find_element(By.NAME, 'new_description').send_keys('Updated description')
        self.driver.find_element(By.NAME, 'new_price').send_keys('15.99')
        self.driver.find_element(By.XPATH, '//button[text()="Update"]').click()
        time.sleep(1)  # Wait for the item to be updated

        # Verify the item is updated
        self.assertIn("Updated Item", self.driver.page_source)

    def test_remove_item_from_wishlist(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Remove an item from the wishlist
        self.driver.find_element(By.NAME, 'item_name').send_keys('item1')
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        time.sleep(1)  # Wait for the item to be removed

        # Verify the item is removed
        self.assertNotIn("item1", self.driver.page_source)

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the logout to complete

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_data_persistence(self):
        # Login and add an item to the wishlist
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'item_name').send_keys('Persistent Item')
        self.driver.find_element(By.NAME, 'description').send_keys('Persistent description')
        self.driver.find_element(By.NAME, 'price').send_keys('20.99')
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        time.sleep(1)  # Wait for the item to be added

        # Logout and close the application
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.driver.quit()
        self.process.terminate()

        # Reopen the application and log back in
        self.setUp()
        self.login("admin", "admin123")

        # Verify the previously added item is still present
        self.assertIn("Persistent Item", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
