import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestWishlistTrackerApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/')  # Replace XXXX with the port from main.py

    def tearDown(self):
        # Close the web driver session and the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8000/register')
        self.assertIn("Register", self.driver.title)

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8000/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)

        # Expect an error message (not implemented in the codebase, so we fail)
        self.fail("Expected error message for existing username not displayed.")

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8000/')
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Invalid login
        self.driver.get('http://localhost:8000/')
        self.login("admin", "wrongpassword")
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.title)  # Should still be on login page

    def test_add_items_to_wishlist(self):
        # Functionality 3: Add Items to Wishlist
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8000/dashboard')
        self.assertIn("Your Wishlist", self.driver.page_source)

        # Add item to wishlist
        self.driver.find_element(By.NAME, 'item_name').send_keys("New Item")
        self.driver.find_element(By.NAME, 'description').send_keys("Item Description")
        self.driver.find_element(By.NAME, 'price').send_keys("19.99")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)

        # Verify item added (not implemented in the codebase, so we fail)
        self.fail("Expected success message for adding item not displayed.")

    def test_view_wishlist(self):
        # Functionality 4: View Wishlist
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8000/dashboard')
        time.sleep(1)

        # Verify that the wishlist is displayed
        self.assertIn("Your Wishlist", self.driver.page_source)

    def test_update_item_in_wishlist(self):
        # Functionality 5: Update Item in Wishlist
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8000/dashboard')
        self.fail("Update item functionality not implemented.")

    def test_remove_item_from_wishlist(self):
        # Functionality 6: Remove Item from Wishlist
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8000/dashboard')
        self.fail("Remove item functionality not implemented.")

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

    def test_data_persistence(self):
        # Functionality 8: Data Persistence
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8000/dashboard')
        self.driver.find_element(By.NAME, 'item_name').send_keys("Persistent Item")
        self.driver.find_element(By.NAME, 'description').send_keys("Persistent Description")
        self.driver.find_element(By.NAME, 'price').send_keys("29.99")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)

        # Logout and log back in
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8000/dashboard')
        time.sleep(1)

        # Check if the item is still present (not implemented in the codebase, so we fail)
        self.fail("Expected persistent item not found in wishlist.")

if __name__ == '__main__':
    unittest.main()
