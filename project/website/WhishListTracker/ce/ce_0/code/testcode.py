import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestWishlistTrackerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8286/')  # Access the login page

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
        # Test user registration functionality
        self.driver.get('http://localhost:8286/register')  # Navigate to registration page

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8286/register')  # Navigate to registration page again
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the error message is displayed
        self.assertIn("Username already exists!", self.driver.page_source)

    def test_login(self):
        # Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Test invalid login
        self.driver.get('http://localhost:8286/')  # Navigate to login page again
        self.login("invalid_user", "wrong_password")

        # Verify the error message is displayed
        self.assertIn("Invalid credentials!", self.driver.page_source)

    def test_add_items_to_wishlist(self):
        # Test adding items to the wishlist
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8286/dashboard')  # Navigate to dashboard

        # Add an item to the wishlist
        self.driver.find_element(By.NAME, 'item_name').send_keys("item3")
        self.driver.find_element(By.NAME, 'description').send_keys("A new gadget")
        self.driver.find_element(By.NAME, 'price').send_keys("29.99")
        self.driver.find_element(By.NAME, 'add_item').click()

        # Verify the item is added to the wishlist
        self.assertIn("item3", self.driver.page_source)

        # Attempt to add an item with missing required fields
        self.driver.find_element(By.NAME, 'item_name').clear()  # Clear item name
        self.driver.find_element(By.NAME, 'add_item').click()

        # Verify the error message is displayed
        self.assertIn("This field is required.", self.driver.page_source)

    def test_view_wishlist(self):
        # Test viewing the wishlist
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8286/dashboard')  # Navigate to dashboard

        # Verify that the wishlist is displayed
        self.assertIn("item1", self.driver.page_source)
        self.assertIn("item2", self.driver.page_source)

    def test_update_item_in_wishlist(self):
        # Test updating an item in the wishlist
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8286/dashboard')  # Navigate to dashboard

        # Update an item
        self.driver.find_element(By.XPATH, '//li[contains(text(), "item1")]').click()  # Select item1
        self.driver.find_element(By.NAME, 'description').clear()
        self.driver.find_element(By.NAME, 'description').send_keys("Updated description")
        self.driver.find_element(By.NAME, 'price').clear()
        self.driver.find_element(By.NAME, 'price').send_keys("19.99")
        self.driver.find_element(By.NAME, 'add_item').click()  # Submit the update

        # Verify the item is updated
        self.assertIn("Updated description", self.driver.page_source)

    def test_remove_item_from_wishlist(self):
        # Test removing an item from the wishlist
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8286/dashboard')  # Navigate to dashboard

        # Remove an item
        self.driver.find_element(By.XPATH, '//li[contains(text(), "item1")]').click()  # Select item1
        self.driver.find_element(By.NAME, 'remove_item').click()  # Assuming there's a remove button

        # Verify the item is removed
        self.assertNotIn("item1", self.driver.page_source)

    def test_data_persistence(self):
        # Test data persistence
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8286/dashboard')  # Navigate to dashboard

        # Add an item to the wishlist
        self.driver.find_element(By.NAME, 'item_name').send_keys("item4")
        self.driver.find_element(By.NAME, 'description').send_keys("Another gadget")
        self.driver.find_element(By.NAME, 'price').send_keys("39.99")
        self.driver.find_element(By.NAME, 'add_item').click()

        # Logout
        self.driver.get('http://localhost:8286/')  # Navigate to login page
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Login again
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8286/dashboard')  # Navigate to dashboard

        # Verify the previously added item is still present
        self.assertIn("item4", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
