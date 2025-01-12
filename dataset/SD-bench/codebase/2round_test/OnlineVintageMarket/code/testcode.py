import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineVintageMarket(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8072')

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

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "adminpass")
        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "unique_user"
        new_password = "unique_password"

        # Input username and password for registration
        self.driver.find_element(By.ID, 'username').send_keys(new_username)
        self.driver.find_element(By.ID, 'password').send_keys(new_password)
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

    def test_search_specific_vintage_item(self):
        # Functionalities 4: Test searching for a specific vintage item by name
        self.login("admin", "adminpass")
        # Search for an item
        item_name = "Vintage Clock"
        self.driver.find_element(By.LINK_TEXT, item_name).click()
        time.sleep(1)  # Wait for the item details page to load
        # Verify the item details page displays the correct item
        self.assertIn(item_name, self.driver.page_source)

    def test_view_item_details(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("admin", "adminpass")
        # Click on an item to view details
        self.driver.find_element(By.LINK_TEXT, 'Vintage Clock').click()
        time.sleep(1)  # Wait for the item details page to load
        # Verify the item details page displays the correct information
        self.assertIn("Vintage Clock", self.driver.page_source)

    def test_create_new_listing(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'List a New Item').click()
        time.sleep(1)  # Wait for the listing page to load

        item_name = "Unique Vintage Item"
        item_description = "A unique vintage item description."
        item_price = "200.00"

        # Fill out the new item form
        self.driver.find_element(By.ID, 'name').send_keys(item_name)
        self.driver.find_element(By.ID, 'description').send_keys(item_description)
        self.driver.find_element(By.ID, 'price').send_keys(item_price)
        self.driver.find_element(By.XPATH, '//button[text()="List Item"]').click()
        time.sleep(1)  # Wait for the home page to load

        # Verify that the new item is displayed on the Home Page
        self.assertIn(item_name, self.driver.page_source)

    def test_submit_item_listing(self):
        # Functionalities 7: Test submitting a valid item listing
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'List a New Item').click()
        time.sleep(1)  # Wait for the listing page to load

        item_name = "Another Unique Item"
        item_description = "Another unique item description."
        item_price = "250.00"

        # Fill out the new item form
        self.driver.find_element(By.ID, 'name').send_keys(item_name)
        self.driver.find_element(By.ID, 'description').send_keys(item_description)
        self.driver.find_element(By.ID, 'price').send_keys(item_price)
        self.driver.find_element(By.XPATH, '//button[text()="List Item"]').click()
        time.sleep(1)  # Wait for the home page to load

        # Verify that the new item is displayed on the Home Page
        self.assertIn(item_name, self.driver.page_source)

    def test_view_detailed_information(self):
        # Functionalities 8: Test viewing detailed information about a vintage item
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Vintage Clock').click()
        time.sleep(1)  # Wait for the item details page to load
        # Verify the item details page displays the correct information
        self.assertIn("Vintage Clock", self.driver.page_source)

    def test_navigate_back_to_home(self):
        # Functionalities 9: Test navigating back to Home Page from Item Details Page
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Vintage Clock').click()
        time.sleep(1)  # Wait for the item details page to load
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the home page to load
        # Verify that the Home Page is displayed
        self.assertIn("Available Vintage Items", self.driver.page_source)

    def test_data_storage(self):
        # Functionalities 10: Test data storage in local text files
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'List a New Item').click()
        time.sleep(1)  # Wait for the listing page to load

        item_name = "Stored Vintage Item"
        item_description = "Stored vintage item description."
        item_price = "300.00"

        # Fill out the new item form
        self.driver.find_element(By.ID, 'name').send_keys(item_name)
        self.driver.find_element(By.ID, 'description').send_keys(item_description)
        self.driver.find_element(By.ID, 'price').send_keys(item_price)
        self.driver.find_element(By.XPATH, '//button[text()="List Item"]').click()
        time.sleep(1)  # Wait for the home page to load

        # Verify that the new item is stored in the local text file
        with open('items.txt', 'r') as file:
            content = file.read()
            self.assertIn(item_name, content)

if __name__ == '__main__':
    unittest.main()
