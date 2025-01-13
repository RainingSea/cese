import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineVintageMarket(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8072/')  # Access the login page

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

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "adminpass")

        # Verify that the Home Page has loaded
        self.assertIn("Available Vintage Items", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
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

    def test_view_available_vintage_items(self):
        # Functionalities 3: Test viewing available vintage items
        self.login("admin", "adminpass")

        # Verify that the Home Page shows items
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No vintage items found.")

    def test_search_vintage_item_by_name(self):
        # Functionalities 4: Test searching for a specific vintage item by name
        self.login("admin", "adminpass")

        # Search for a specific item
        item_name = "Vintage Clock"
        self.driver.find_element(By.LINK_TEXT, item_name).click()
        time.sleep(1)  # Wait for the item details page to load

        # Verify that the item details page shows the correct item
        self.assertIn(item_name, self.driver.page_source)

    def test_view_item_details(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("admin", "adminpass")

        # Click on an item to view details
        item_name = "Vintage Clock"
        self.driver.find_element(By.LINK_TEXT, item_name).click()
        time.sleep(1)  # Wait for the item details page to load

        # Verify that the item details are displayed
        self.assertIn("Description", self.driver.page_source)
        self.assertIn("Price", self.driver.page_source)

    def test_create_new_listing(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.login("admin", "adminpass")

        # Navigate to the Listing Page
        self.driver.find_element(By.LINK_TEXT, 'List a New Item').click()
        time.sleep(1)  # Wait for the listing page to load

        # Fill out the new item form
        item_name = "New Vintage Item"
        item_description = "A description of the new vintage item."
        item_price = "100.00"

        self.driver.find_element(By.NAME, 'name').send_keys(item_name)
        self.driver.find_element(By.NAME, 'description').send_keys(item_description)
        self.driver.find_element(By.NAME, 'price').send_keys(item_price)
        self.driver.find_element(By.XPATH, '//button[text()="List Item"]').click()
        time.sleep(1)  # Wait for the home page to load

        # Verify that the new item is displayed on the Home Page
        self.assertIn(item_name, self.driver.page_source)

    def test_submit_item_listing(self):
        # Functionalities 7: Test submitting a valid item listing
        self.login("admin", "adminpass")

        # Navigate to the Listing Page
        self.driver.find_element(By.LINK_TEXT, 'List a New Item').click()
        time.sleep(1)  # Wait for the listing page to load

        # Fill out the new item form
        item_name = "Another Vintage Item"
        item_description = "A description of another vintage item."
        item_price = "150.00"

        self.driver.find_element(By.NAME, 'name').send_keys(item_name)
        self.driver.find_element(By.NAME, 'description').send_keys(item_description)
        self.driver.find_element(By.NAME, 'price').send_keys(item_price)
        self.driver.find_element(By.XPATH, '//button[text()="List Item"]').click()
        time.sleep(1)  # Wait for the home page to load

        # Verify that the new item is displayed on the Home Page
        self.assertIn(item_name, self.driver.page_source)

    def test_view_detailed_information_about_item(self):
        # Functionalities 8: Test viewing detailed information about a vintage item
        self.login("admin", "adminpass")

        # Click on an item to view details
        item_name = "Vintage Clock"
        self.driver.find_element(By.LINK_TEXT, item_name).click()
        time.sleep(1)  # Wait for the item details page to load

        # Verify that the item details are displayed
        self.assertIn("Description", self.driver.page_source)
        self.assertIn("Price", self.driver.page_source)

    def test_navigate_back_to_home_from_item_details(self):
        # Functionalities 9: Test navigating back to home page from item details page
        self.login("admin", "adminpass")

        # Click on an item to view details
        item_name = "Vintage Clock"
        self.driver.find_element(By.LINK_TEXT, item_name).click()
        time.sleep(1)  # Wait for the item details page to load

        # Click the back to home link
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the home page to load

        # Verify that the Home Page is displayed
        self.assertIn("Available Vintage Items", self.driver.page_source)

    def test_data_storage_in_local_text_files(self):
        # Functionalities 10: Test data storage in local text files
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
