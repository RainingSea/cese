import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestShopPalApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8552/login')

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
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8552/login')
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)

    def test_create_personalized_collections(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify the Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to create a collection with an empty name
        # (This functionality is not implemented in the codebase)
        self.fail("Create collection functionality not implemented")

    def test_track_price_changes(self):
        # This functionality is not implemented in the codebase
        self.fail("Track price changes functionality not implemented")

    def test_view_detailed_product_information(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Search for a product using keywords
        # (This functionality is not implemented in the codebase)
        self.fail("View detailed product information functionality not implemented")

    def test_search_for_products(self):
        # This functionality is not implemented in the codebase
        self.fail("Search for products functionality not implemented")

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8552/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # This functionality is not implemented in the codebase
        self.fail("Navigate back to dashboard functionality not implemented")

    def test_receive_notifications_for_discounts(self):
        # This functionality is not implemented in the codebase
        self.fail("Receive notifications for discounts functionality not implemented")

if __name__ == '__main__':
    unittest.main()
