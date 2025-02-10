import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestOnlineVintageMarket(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8560/') 

    def tearDown(self):
        # Close the web driver session and terminate the process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_vintage_items(self):
        # Functionalities 3: Test viewing available vintage items
        self.login("admin", "admin123")

        # Verify that the Home Page shows items
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No vintage items found.")

    def test_search_vintage_item(self):
        # Functionalities 4: Test searching for a specific vintage item by name
        self.login("admin", "admin123")

        search_box = self.driver.find_element(By.XPATH, '//input[@type="text"]')
        search_box.send_keys("Vintage Clock")
        time.sleep(1)  # Simulate search action

        # Verify that the search results contain the specific item
        self.assertIn("Vintage Clock", self.driver.page_source)

    def test_view_item_details(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("admin", "admin123")

        # Click on the first item's details link
        self.driver.find_element(By.LINK_TEXT, 'Item Details').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Item Details Page shows correct information
        self.assertIn("Description", self.driver.page_source)

    def test_create_new_listing(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.login("admin", "admin123")

        # Navigate to the Listing Page
        self.driver.find_element(By.LINK_TEXT, 'List a new item').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the listing form
        self.driver.find_element(By.NAME, 'item_name').send_keys("Test Item")
        self.driver.find_element(By.NAME, 'description').send_keys("Test Description")
        self.driver.find_element(By.NAME, 'price').send_keys("100")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the new item is listed on the Home Page
        self.assertIn("Test Item", self.driver.page_source)

    def test_submit_item_listing(self):
        # Functionalities 7: Test submitting an item listing
        self.login("admin", "admin123")

        # Navigate to the Listing Page
        self.driver.find_element(By.LINK_TEXT, 'List a new item').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the listing form
        self.driver.find_element(By.NAME, 'item_name').send_keys("Another Test Item")
        self.driver.find_element(By.NAME, 'description').send_keys("Another Test Description")
        self.driver.find_element(By.NAME, 'price').send_keys("200")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the new item is listed on the Home Page
        self.assertIn("Another Test Item", self.driver.page_source)

    def test_view_detailed_information(self):
        # Functionalities 8: Test viewing detailed information about a vintage item
        self.login("admin", "admin123")

        # Click on the first item's details link
        self.driver.find_element(By.LINK_TEXT, 'Item Details').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Item Details Page shows correct information
        self.assertIn("Description", self.driver.page_source)

    def test_navigate_back_to_home(self):
        # Functionalities 9: Test navigating back to the Home Page from Item Details Page
        self.login("admin", "admin123")

        # Click on the first item's details link
        self.driver.find_element(By.LINK_TEXT, 'Item Details').click()
        time.sleep(1)  # Wait for the next page to load

        # Click on the "Back" link
        self.driver.find_element(By.LINK_TEXT, 'Back').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Home Page has loaded
        self.assertIn("Vintage Items", self.driver.page_source)

    def test_data_storage(self):
        # Functionalities 10: Test data storage in local text files
        self.login("admin", "admin123")

        # Navigate to the Listing Page
        self.driver.find_element(By.LINK_TEXT, 'List a new item').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the listing form
        item_name = "Storage Test Item"
        self.driver.find_element(By.NAME, 'item_name').send_keys(item_name)
        self.driver.find_element(By.NAME, 'description').send_keys("Storage Test Description")
        self.driver.find_element(By.NAME, 'price').send_keys("300")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the new item is saved in the items.txt file
        with open('items.txt', 'r') as file:
            self.assertIn(item_name, file.read())

if __name__ == '__main__':
    unittest.main()
