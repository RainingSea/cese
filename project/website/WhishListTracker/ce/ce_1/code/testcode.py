import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestWishlistTrackerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8459/')  # Access the login page

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
        self.driver.get('http://localhost:8459/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8459/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify registration failed
        self.assertIn("Registration failed", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8459/')  # Navigate to login page
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Invalid login
        self.driver.get('http://localhost:8459/')  # Navigate to login page again
        self.login("admin", "wrongpassword")
        self.assertIn("Login failed", self.driver.page_source)

    def test_add_items_to_wishlist(self):
        # Functionality 3: Add Items to Wishlist
        self.login("user1", "user123")  # Login as user1
        self.assertIn("Dashboard", self.driver.title)

        # Add item to wishlist
        self.driver.find_element(By.NAME, 'item_name').send_keys("New Item")
        self.driver.find_element(By.NAME, 'description').send_keys("Item Description")
        self.driver.find_element(By.NAME, 'price').send_keys("100.00")
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()

        # Verify item was added
        self.assertIn("New Item", self.driver.page_source)

        # Attempt to add an item with missing fields
        self.driver.find_element(By.NAME, 'item_name').clear()  # Clear item name
        self.driver.find_element(By.NAME, 'description').send_keys("Another Item Description")
        self.driver.find_element(By.NAME, 'price').send_keys("50.00")
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()

        # Verify error message for missing item name
        self.assertIn("This field is required.", self.driver.page_source)

    def test_view_wishlist(self):
        # Functionality 4: View Wishlist
        self.login("user1", "user123")  # Login as user1
        self.assertIn("Dashboard", self.driver.title)

        # Verify wishlist is displayed
        self.assertIn("New Phone", self.driver.page_source)
        self.assertIn("Book", self.driver.page_source)

    def test_remove_item_from_wishlist(self):
        # Functionality 6: Remove Item from Wishlist
        self.login("user1", "user123")  # Login as user1
        self.assertIn("Dashboard", self.driver.title)

        # Remove an item from the wishlist
        self.driver.find_element(By.XPATH, '//li[contains(text(), "New Phone")]/form/button').click()

        # Verify item was removed
        self.assertNotIn("New Phone", self.driver.page_source)

        # Attempt to remove an item that does not exist
        self.driver.find_element(By.XPATH, '//li[contains(text(), "Nonexistent Item")]/form/button').click()
        self.assertIn("Item cannot be found", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Login as admin
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_data_persistence(self):
        # Functionality 8: Data Persistence
        self.login("user1", "user123")  # Login as user1
        self.driver.find_element(By.NAME, 'item_name').send_keys("Persistent Item")
        self.driver.find_element(By.NAME, 'description').send_keys("Persistent Item Description")
        self.driver.find_element(By.NAME, 'price').send_keys("200.00")
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()

        # Logout and log back in
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.login("user1", "user123")

        # Verify the previously added item is still present
        self.assertIn("Persistent Item", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
