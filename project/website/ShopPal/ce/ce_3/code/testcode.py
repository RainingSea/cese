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
        self.driver.get('http://localhost:8695/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the app process
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
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)

        # Expectation: Error message for existing username
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify redirection to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8695/')
        self.login("invalid_user", "wrong_password")

        # Expectation: Redirect back to login page
        self.assertIn("Login", self.driver.title)

    def test_create_personalized_collections(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to create a collection with an empty name
        self.driver.find_element(By.XPATH, '//input[@value="Add Product"]').click()
        time.sleep(1)

        # Expectation: Error message for empty collection name
        self.assertIn("Dashboard", self.driver.title)

    def test_track_price_changes(self):
        # This functionality is not implemented in the codebase
        self.fail("Track Price Changes functionality not implemented")

    def test_view_detailed_product_information(self):
        # This functionality is not implemented in the codebase
        self.fail("View Detailed Product Information functionality not implemented")

    def test_search_for_products(self):
        # This functionality is not implemented in the codebase
        self.fail("Search for Products functionality not implemented")

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Logout from the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8695/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # This functionality is not implemented in the codebase
        self.fail("Navigate Back to Dashboard functionality not implemented")

    def test_receive_notifications_for_discounts(self):
        # This functionality is not implemented in the codebase
        self.fail("Receive Notifications for Discounts functionality not implemented")

if __name__ == '__main__':
    unittest.main()
