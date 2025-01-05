import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineVintageMarket(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8101/')  # Access the login page

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
        self.login("admin", "adminpass")
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No vintage items found.")

    def test_search_specific_vintage_item(self):
        # Functionalities 4: Test searching for a specific vintage item
        self.login("admin", "adminpass")
        item_name = "Vintage Clock"
        item_link = self.driver.find_element(By.LINK_TEXT, item_name)
        self.assertIsNotNone(item_link, f"Item '{item_name}' not found.")

    def test_view_item_details(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("admin", "adminpass")
        item_name = "Vintage Clock"
        self.driver.find_element(By.LINK_TEXT, item_name).click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn(item_name, self.driver.page_source)

    def test_create_new_listing(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Add New Item').click()
        time.sleep(1)  # Wait for the next page to load

        item_name = "New Vintage Item"
        item_description = "A description of the new vintage item"
        item_price = "99.99"

        self.driver.find_element(By.NAME, 'name').send_keys(item_name)
        self.driver.find_element(By.NAME, 'description').send_keys(item_description)
        self.driver.find_element(By.NAME, 'price').send_keys(item_price)
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Home", self.driver.title)

    def test_submit_item_listing(self):
        # Functionalities 7: Test submitting an item listing
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Add New Item').click()
        time.sleep(1)  # Wait for the next page to load

        item_name = "Submitted Vintage Item"
        item_description = "Description of the submitted vintage item"
        item_price = "150.00"

        self.driver.find_element(By.NAME, 'name').send_keys(item_name)
        self.driver.find_element(By.NAME, 'description').send_keys(item_description)
        self.driver.find_element(By.NAME, 'price').send_keys(item_price)
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Home", self.driver.title)

    def test_view_detailed_information(self):
        # Functionalities 8: Test viewing detailed information about a vintage item
        self.login("admin", "adminpass")
        item_name = "Vintage Clock"
        self.driver.find_element(By.LINK_TEXT, item_name).click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn(item_name, self.driver.page_source)

    def test_navigate_back_to_home(self):
        # Functionalities 9: Test navigating back to the home page from item details
        self.login("admin", "adminpass")
        item_name = "Vintage Clock"
        self.driver.find_element(By.LINK_TEXT, item_name).click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Home", self.driver.title)

    def test_data_storage(self):
        # Functionalities 10: Test data storage in local text files
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Add New Item').click()
        time.sleep(1)  # Wait for the next page to load

        item_name = "Stored Vintage Item"
        item_description = "Description of the stored vintage item"
        item_price = "200.00"

        self.driver.find_element(By.NAME, 'name').send_keys(item_name)
        self.driver.find_element(By.NAME, 'description').send_keys(item_description)
        self.driver.find_element(By.NAME, 'price').send_keys(item_price)
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        time.sleep(1)  # Wait for the next page to load

        with open('items.txt', 'r') as f:
            self.assertIn(item_name, f.read())

if __name__ == '__main__':
    unittest.main()
