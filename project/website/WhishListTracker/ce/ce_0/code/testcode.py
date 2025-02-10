import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestWishlistApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8698/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and stop the application
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
        time.sleep(1)  # Wait for the next page to load

        # Verify the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)  # Assuming the page reloads with an error

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8698/')  # Navigate back to the login page
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)  # Assuming the page reloads with an error

    def test_add_items_to_wishlist(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Enter item name, description, and desired price, then submit the form
        self.driver.find_element(By.NAME, 'name').send_keys("New Item")
        self.driver.find_element(By.NAME, 'description').send_keys("New Description")
        self.driver.find_element(By.NAME, 'price').send_keys("20.99")
        self.driver.find_element(By.NAME, 'add_item').click()
        time.sleep(1)  # Wait for the item to be added

        # Verify the item is added to the wishlist
        self.assertIn("New Item", self.driver.page_source)

        # Attempt to add an item with missing required fields
        self.driver.find_element(By.NAME, 'name').clear()
        self.driver.find_element(By.NAME, 'add_item').click()
        time.sleep(1)  # Wait for the error message

        # Verify an error message is displayed
        self.assertIn("Dashboard", self.driver.title)  # Assuming the page reloads with an error

    def test_view_wishlist(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Verify the wishlist is displayed
        items = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(items), 0, "No items found in the wishlist.")

        # Refresh the Dashboard Page after adding a new item
        self.driver.refresh()
        time.sleep(1)  # Wait for the page to reload

        # Verify the newly added item appears in the wishlist
        self.assertIn("Item 1", self.driver.page_source)

    def test_update_item_in_wishlist(self):
        # Functionality not implemented in the codebase
        self.fail("Update item functionality not implemented")

    def test_remove_item_from_wishlist(self):
        # Functionality not implemented in the codebase
        self.fail("Remove item functionality not implemented")

    def test_user_logout(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the Dashboard Page after logging out
        self.driver.get('http://localhost:8698/dashboard')
        time.sleep(1)  # Wait for the page to load

        # Verify access to the Dashboard is denied
        self.assertIn("Login", self.driver.title)

    def test_data_persistence(self):
        # Functionality not implemented in the codebase
        self.fail("Data persistence functionality not implemented")

if __name__ == '__main__':
    unittest.main()
