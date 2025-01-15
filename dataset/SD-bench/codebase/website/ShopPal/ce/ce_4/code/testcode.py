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
        self.driver.get('http://localhost:8696/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.ID, 'username').send_keys(new_username)
        self.driver.find_element(By.ID, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.ID, 'username').send_keys("admin")
        self.driver.find_element(By.ID, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)  # Assuming it stays on the same page

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8696/')  # Navigate back to login page
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)  # Assuming it stays on the same page

    def test_create_personalized_collections(self):
        # This functionality is not implemented in the codebase
        self.fail("Create Personalized Collections functionality not implemented")

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
        # Login first
        self.login("admin", "admin123")

        # Click the Logout button
        # This functionality is not implemented in the codebase
        self.fail("User Logout functionality not implemented")

    def test_navigate_back_to_dashboard(self):
        # This functionality is not implemented in the codebase
        self.fail("Navigate Back to Dashboard functionality not implemented")

    def test_receive_notifications_for_discounts(self):
        # This functionality is not implemented in the codebase
        self.fail("Receive Notifications for Discounts functionality not implemented")

if __name__ == '__main__':
    unittest.main()
