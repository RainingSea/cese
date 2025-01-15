import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestWishListTrackerApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8564/login')

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
        # Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Enter new user details
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("Username is already taken", self.driver.page_source)

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Test invalid login
        self.driver.get('http://localhost:8564/login')
        self.login("invalid_user", "wrong_password")

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_add_items_to_wishlist(self):
        # Test adding items to wishlist
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Add a new item
        self.driver.find_element(By.NAME, 'item_name').send_keys("Smartphone")
        self.driver.find_element(By.NAME, 'item_description').send_keys("Latest model")
        self.driver.find_element(By.NAME, 'item_price').send_keys("999.99")
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        time.sleep(1)

        # Verify the item is added
        self.assertIn("Smartphone", self.driver.page_source)

        # Attempt to add an item with missing fields
        self.driver.find_element(By.NAME, 'item_name').clear()
        self.driver.find_element(By.NAME, 'item_description').clear()
        self.driver.find_element(By.NAME, 'item_price').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        time.sleep(1)

        # Verify error message for missing fields
        self.assertIn("This field is required", self.driver.page_source)

    def test_view_wishlist(self):
        # Test viewing wishlist
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows items
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No wishlist items found.")

        # Refresh the page and verify items persist
        self.driver.refresh()
        time.sleep(1)
        self.assertIn("Laptop", self.driver.page_source)

    def test_update_item_in_wishlist(self):
        # Test updating an item in the wishlist
        self.login("admin", "admin123")

        # Update an existing item
        self.driver.find_element(By.XPATH, '//form[@action="/update_item/Laptop"]//input[@name="item_description"]').send_keys("Updated description")
        self.driver.find_element(By.XPATH, '//form[@action="/update_item/Laptop"]//input[@name="item_price"]').send_keys("1100.00")
        self.driver.find_element(By.XPATH, '//form[@action="/update_item/Laptop"]//button[text()="Update"]').click()
        time.sleep(1)

        # Verify the item is updated
        self.assertIn("Updated description", self.driver.page_source)

    def test_remove_item_from_wishlist(self):
        # Test removing an item from the wishlist
        self.login("admin", "admin123")

        # Remove an existing item
        self.driver.find_element(By.XPATH, '//form[@action="/remove_item/Headphones"]//button[text()="Remove"]').click()
        time.sleep(1)

        # Verify the item is removed
        self.assertNotIn("Headphones", self.driver.page_source)

    def test_user_logout(self):
        # Test user logout functionality
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard after logging out
        self.driver.get('http://localhost:8564/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_data_persistence(self):
        # Test data persistence
        self.login("admin", "admin123")

        # Add a new item
        self.driver.find_element(By.NAME, 'item_name').send_keys("Tablet")
        self.driver.find_element(By.NAME, 'item_description').send_keys("New tablet")
        self.driver.find_element(By.NAME, 'item_price').send_keys("499.99")
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        time.sleep(1)

        # Logout and close the application
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.driver.quit()
        self.process.terminate()

        # Reopen the application and log back in
        self.setUp()
        self.login("admin", "admin123")

        # Verify the item is still present
        self.assertIn("Tablet", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
