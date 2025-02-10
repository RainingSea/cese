import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestShopPalApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8694/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and stop the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that an error message is displayed
        self.assertIn("Register", self.driver.title)  # Assuming the page stays the same on error

    def test_user_login(self):
        # Verify that the Login form is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8694/')  # Navigate back to the login page
        self.login("invalid_user", "wrong_password")

        # Verify that an error message is displayed
        self.assertIn("Login", self.driver.title)  # Assuming the page stays the same on error

    def test_create_personalized_collections(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify that the Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Create a new collection by entering a collection name and saving it
        # Assuming there is a form to create collections (not implemented in the codebase)
        self.fail("Create collection functionality not implemented")

    def test_track_price_changes(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Add a product to a collection and enable price tracking
        # Assuming there is a functionality to add products and track prices (not implemented in the codebase)
        self.fail("Price tracking functionality not implemented")

    def test_view_detailed_product_information(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Search for a product using keywords
        # Assuming there is a search functionality (not implemented in the codebase)
        self.fail("Product search functionality not implemented")

    def test_search_for_products(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Navigate to the search bar and enter a keyword
        # Assuming there is a search functionality (not implemented in the codebase)
        self.fail("Product search functionality not implemented")

    def test_user_logout(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8694/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click on a product to view its detailed information
        # Assuming there is a functionality to view product details (not implemented in the codebase)
        self.fail("Navigate back to dashboard functionality not implemented")

    def test_receive_notifications_for_discounts(self):
        # Login successfully and navigate to a product in a collection
        self.login("admin", "admin123")

        # Enable notifications for price drops on that product
        # Assuming there is a functionality to enable notifications (not implemented in the codebase)
        self.fail("Notifications for discounts functionality not implemented")

if __name__ == '__main__':
    unittest.main()
