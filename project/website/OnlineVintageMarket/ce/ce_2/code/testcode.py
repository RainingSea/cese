import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time
import os

class TestOnlineVintageMarket(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8964/') 

    def tearDown(self):
        # Close the web driver session and terminate the web application
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
        self.login("admin", "admin123")

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
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

    def test_view_available_vintage_items(self):
        # Functionalities 3: Test viewing available vintage items
        self.login("admin", "admin123")

        # Verify that the Home Page shows items
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No vintage items found.")

    def test_search_vintage_item_by_name(self):
        # Functionalities 4: Test searching for a specific vintage item by name
        self.fail("not implemented")

    def test_view_item_details(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("admin", "admin123")

        # Click on the first item link
        item_link = self.driver.find_element(By.TAG_NAME, 'a')
        item_name = item_link.text
        item_link.click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Item Details Page shows correct information
        self.assertIn(item_name, self.driver.page_source)

    def test_create_new_listing(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add New Item').click()
        time.sleep(1)  # Wait for the next page to load

        item_name = "Vintage Lamp"
        item_description = "A beautiful vintage lamp."
        item_price = "60.00"

        # Fill out the new item form
        self.driver.find_element(By.NAME, 'name').send_keys(item_name)
        self.driver.find_element(By.NAME, 'description').send_keys(item_description)
        self.driver.find_element(By.NAME, 'price').send_keys(item_price)
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the new item is displayed on the Home Page
        self.assertIn(item_name, self.driver.page_source)

    def test_submit_item_listing(self):
        # Functionalities 7: Test submitting an item listing
        self.fail("not implemented")

    def test_view_detailed_information(self):
        # Functionalities 8: Test viewing detailed information about a vintage item
        self.fail("not implemented")

    def test_navigate_back_to_home(self):
        # Functionalities 9: Test navigating back to the Home Page from Item Details Page
        self.login("admin", "admin123")

        # Click on the first item link
        item_link = self.driver.find_element(By.TAG_NAME, 'a')
        item_link.click()
        time.sleep(1)  # Wait for the next page to load

        # Click on the "Back to Home" link
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_data_storage(self):
        # Functionalities 10: Test data storage in local text files
        self.fail("not implemented")

if __name__ == '__main__':
    unittest.main()
