import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestShopPalApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8411/')  # Access the login page

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
        self.driver.get('http://localhost:8411/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8411/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8411/')
        self.login("admin", "wrong_password")
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_create_collection(self):
        # Functionality 3: Create Personalized Collections
        self.login("admin", "admin123")  # Login successfully

        # Verify that the Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to create a new collection
        self.driver.find_element(By.NAME, 'product_id').send_keys("1")  # Assuming product ID 1 exists
        self.driver.find_element(By.XPATH, '//button[text()="Add to Collection"]').click()
        time.sleep(1)  # Wait for the action to complete

        # Verify that the collection was added
        self.assertIn("Product A", self.driver.page_source)

        # Attempt to create a collection with an empty name (not applicable in current implementation)
        # This test point will fail as the functionality is not implemented
        self.fail("Creating a collection with an empty name is not implemented.")

    def test_track_price_changes(self):
        # Functionality 4: Track Price Changes
        self.login("admin", "admin123")  # Login successfully

        # Attempt to track price changes (not implemented)
        self.fail("Tracking price changes functionality is not implemented.")

    def test_view_product_details(self):
        # Functionality 5: View Detailed Product Information
        self.login("admin", "admin123")  # Login successfully

        # Search for a product (assuming search functionality is available)
        self.driver.find_element(By.NAME, 'search').send_keys("Product A")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        # Click on the product to view details
        self.driver.find_element(By.LINK_TEXT, "Product A").click()
        time.sleep(1)  # Wait for the product details page to load

        # Verify product details are displayed
        self.assertIn("Product A", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Login successfully

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 8: Navigate Back to Dashboard
        self.login("admin", "admin123")  # Login successfully

        # Click on a product to view its details
        self.driver.find_element(By.LINK_TEXT, "Product A").click()
        time.sleep(1)  # Wait for the product details page to load

        # Click the back button to return to the Dashboard Page
        self.driver.back()
        time.sleep(1)  # Wait for the Dashboard Page to load

        # Verify that the Dashboard Page is displayed again
        self.assertIn("Dashboard", self.driver.title)

    def test_receive_notifications(self):
        # Functionality 9: Receive Notifications for Discounts
        self.login("admin", "admin123")  # Login successfully

        # Enable notifications for a product (not implemented)
        self.fail("Enabling notifications for discounts is not implemented.")

if __name__ == '__main__':
    unittest.main()
