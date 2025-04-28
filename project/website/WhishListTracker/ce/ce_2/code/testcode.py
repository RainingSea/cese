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
        self.driver.get('http://localhost:8460/')  # Access the login page

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
        self.driver.get('http://localhost:8460/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)  # Check if Registration form is displayed

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8460/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check for error message
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)  # Check if redirected to Dashboard

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8460/')
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Invalid credentials", self.driver.page_source)  # Check for error message

    def test_add_items_to_wishlist(self):
        # Functionality 3: Add Items to Wishlist
        self.login("admin", "admin123")  # Login successfully
        self.assertIn("Dashboard", self.driver.title)  # Check if Dashboard is displayed

        # Add a new item
        self.driver.find_element(By.NAME, 'item_name').send_keys("New Item")
        self.driver.find_element(By.NAME, 'description').send_keys("New Item Description")
        self.driver.find_element(By.NAME, 'price').send_keys("100.00")
        self.driver.find_element(By.NAME, 'add').click()
        time.sleep(1)  # Wait for the item to be added

        # Verify the item is added
        self.assertIn("New Item", self.driver.page_source)

        # Attempt to add an item with missing fields
        self.driver.find_element(By.NAME, 'item_name').clear()  # Clear item name
        self.driver.find_element(By.NAME, 'description').send_keys("Missing Item Name")
        self.driver.find_element(By.NAME, 'price').send_keys("50.00")
        self.driver.find_element(By.NAME, 'add').click()
        time.sleep(1)  # Wait for the error

        # Check for error message
        self.assertIn("All fields are required", self.driver.page_source)

    def test_view_wishlist(self):
        # Functionality 4: View Wishlist
        self.login("admin", "admin123")  # Login successfully
        self.assertIn("Dashboard", self.driver.title)  # Check if Dashboard is displayed

        # Verify that the wishlist is displayed
        items = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(items), 0, "No items found in the wishlist.")

    def test_update_item_in_wishlist(self):
        # Functionality 5: Update Item in Wishlist
        self.login("admin", "admin123")  # Login successfully
        self.driver.find_element(By.NAME, 'item_name').send_keys("Item to Update")
        self.driver.find_element(By.NAME, 'description').send_keys("Description")
        self.driver.find_element(By.NAME, 'price').send_keys("200.00")
        self.driver.find_element(By.NAME, 'add').click()
        time.sleep(1)  # Wait for the item to be added

        # Update the item
        self.driver.find_element(By.NAME, 'item_name').clear()
        self.driver.find_element(By.NAME, 'item_name').send_keys("Item to Update")
        self.driver.find_element(By.NAME, 'description').clear()
        self.driver.find_element(By.NAME, 'description').send_keys("Updated Description")
        self.driver.find_element(By.NAME, 'price').clear()
        self.driver.find_element(By.NAME, 'price').send_keys("250.00")
        self.driver.find_element(By.NAME, 'update').click()
        time.sleep(1)  # Wait for the item to be updated

        # Verify the item is updated
        self.assertIn("Updated Description", self.driver.page_source)

    def test_remove_item_from_wishlist(self):
        # Functionality 6: Remove Item from Wishlist
        self.login("admin", "admin123")  # Login successfully
        self.driver.find_element(By.NAME, 'item_name').send_keys("Item to Remove")
        self.driver.find_element(By.NAME, 'description').send_keys("Description")
        self.driver.find_element(By.NAME, 'price').send_keys("300.00")
        self.driver.find_element(By.NAME, 'add').click()
        time.sleep(1)  # Wait for the item to be added

        # Remove the item
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        time.sleep(1)  # Wait for the item to be removed

        # Verify the item is removed
        self.assertNotIn("Item to Remove", self.driver.page_source)

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
        self.driver.find_element(By.NAME, 'item_name').send_keys("Persistent Item")
        self.driver.find_element(By.NAME, 'description').send_keys("Persistent Description")
        self.driver.find_element(By.NAME, 'price').send_keys("400.00")
        self.driver.find_element(By.NAME, 'add').click()
        time.sleep(1)  # Wait for the item to be added

        # Logout and close the application
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Reopen the application and log back in
        self.driver.get('http://localhost:8460/')
        self.login("admin", "admin123")  # Login successfully

        # Verify the previously added item is still present
        self.assertIn("Persistent Item", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
