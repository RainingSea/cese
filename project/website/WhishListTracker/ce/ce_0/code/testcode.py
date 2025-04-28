import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestWishlistTrackerApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8458/') 

    def tearDown(self):
        # Close the web driver session and the application
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
        self.driver.get('http://localhost:8458/register')
        time.sleep(1)  # Wait for the registration page to load

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
        self.driver.get('http://localhost:8458/register')
        time.sleep(1)  # Wait for the registration page to load
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8458/')
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8458/')
        self.login("admin", "wrongpassword")
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for incorrect credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_add_items_to_wishlist(self):
        # Functionality 3: Add Items to Wishlist
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8458/dashboard')
        time.sleep(1)  # Wait for the dashboard to load

        # Add a new item
        self.driver.find_element(By.NAME, 'name').send_keys("New Laptop")
        self.driver.find_element(By.NAME, 'description').send_keys("High-end gaming laptop")
        self.driver.find_element(By.NAME, 'price').send_keys("1500.00")
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        time.sleep(1)  # Wait for the item to be added

        # Verify that the item appears in the wishlist
        self.assertIn("New Laptop", self.driver.page_source)

        # Attempt to add an item with missing fields
        self.driver.find_element(By.NAME, 'name').clear()  # Clear the name field
        self.driver.find_element(By.NAME, 'description').send_keys("Missing name")
        self.driver.find_element(By.NAME, 'price').send_keys("1000.00")
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        time.sleep(1)  # Wait for the error message

        # Verify error message for missing fields
        self.assertIn("All fields are required", self.driver.page_source)

    def test_view_wishlist(self):
        # Functionality 4: View Wishlist
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8458/dashboard')
        time.sleep(1)  # Wait for the dashboard to load

        # Verify that the wishlist is displayed
        self.assertIn("Gaming Laptop", self.driver.page_source)

    def test_remove_item_from_wishlist(self):
        # Functionality 6: Remove Item from Wishlist
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8458/dashboard')
        time.sleep(1)  # Wait for the dashboard to load

        # Remove an item
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        time.sleep(1)  # Wait for the item to be removed

        # Verify that the item is no longer in the wishlist
        self.assertNotIn("Gaming Laptop", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_data_persistence(self):
        # Functionality 8: Data Persistence
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8458/dashboard')
        time.sleep(1)  # Wait for the dashboard to load

        # Add an item to the wishlist
        self.driver.find_element(By.NAME, 'name').send_keys("Persistent Item")
        self.driver.find_element(By.NAME, 'description').send_keys("This item should persist")
        self.driver.find_element(By.NAME, 'price').send_keys("200.00")
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        time.sleep(1)  # Wait for the item to be added

        # Logout and close the application
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Restart the application
        self.process.terminate()
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver.get('http://localhost:8458/')
        time.sleep(1)  # Wait for the application to start

        # Login again
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8458/dashboard')
        time.sleep(1)  # Wait for the dashboard to load

        # Verify that the previously added item is still present
        self.assertIn("Persistent Item", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
