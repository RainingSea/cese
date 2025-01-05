import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineVintageMarket(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8100/')  # Access the login page

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
        self.login("admin", "pass123")

        # Verify that the Home Page has loaded
        self.assertIn("Vintage Items", self.driver.page_source)

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
        self.login("admin", "pass123")

        # Verify that the Home Page shows items
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No vintage items found.")

    def test_search_for_specific_vintage_item(self):
        # Functionalities 4: Test searching for a specific vintage item
        self.login("admin", "pass123")

        # Search for an item by clicking on it
        self.driver.find_element(By.LINK_TEXT, 'Vintage Clock').click()
        time.sleep(1)  # Wait for the item details page to load

        # Verify that the item details page shows the correct item
        self.assertIn("Vintage Clock", self.driver.page_source)

    def test_view_details_of_selected_item(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("admin", "pass123")

        # Click on an item to view details
        self.driver.find_element(By.LINK_TEXT, 'Vintage Clock').click()
        time.sleep(1)  # Wait for the item details page to load

        # Verify that the item details page shows the correct information
        self.assertIn("A beautiful vintage clock.", self.driver.page_source)

    def test_create_new_listing_for_vintage_items(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.login("admin", "pass123")

        # Navigate to the Listing Page
        self.driver.find_element(By.LINK_TEXT, 'Add New Item').click()
        time.sleep(1)  # Wait for the listing page to load

        # Fill out the new item form
        self.driver.find_element(By.NAME, 'name').send_keys("New Vintage Item")
        self.driver.find_element(By.NAME, 'description').send_keys("A description for the new vintage item.")
        self.driver.find_element(By.NAME, 'price').send_keys("99.99")
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        time.sleep(1)  # Wait for the home page to load

        # Verify that the new item is displayed on the Home Page
        self.assertIn("New Vintage Item", self.driver.page_source)

    def test_submit_item_listing(self):
        # Functionalities 7: Test submitting an item listing
        self.login("admin", "pass123")

        # Navigate to the Listing Page
        self.driver.find_element(By.LINK_TEXT, 'Add New Item').click()
        time.sleep(1)  # Wait for the listing page to load

        # Fill out the new item form
        self.driver.find_element(By.NAME, 'name').send_keys("Another Vintage Item")
        self.driver.find_element(By.NAME, 'description').send_keys("Another description.")
        self.driver.find_element(By.NAME, 'price').send_keys("79.99")
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        time.sleep(1)  # Wait for the home page to load

        # Verify that the new item is displayed on the Home Page
        self.assertIn("Another Vintage Item", self.driver.page_source)

    def test_view_detailed_information_about_vintage_item(self):
        # Functionalities 8: Test viewing detailed information about a vintage item
        self.login("admin", "pass123")

        # Click on an item to view details
        self.driver.find_element(By.LINK_TEXT, 'Antique Vase').click()
        time.sleep(1)  # Wait for the item details page to load

        # Verify that the item details page shows the correct information
        self.assertIn("An exquisite antique vase.", self.driver.page_source)

    def test_navigate_back_to_home_page_from_item_details(self):
        # Functionalities 9: Test navigating back to the Home Page from Item Details Page
        self.login("admin", "pass123")

        # Click on an item to view details
        self.driver.find_element(By.LINK_TEXT, 'Antique Vase').click()
        time.sleep(1)  # Wait for the item details page to load

        # Click on the "Back to Home" link
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the home page to load

        # Verify that the Home Page is displayed
        self.assertIn("Vintage Items", self.driver.page_source)

    def test_data_storage_in_local_text_files(self):
        # Functionalities 10: Test data storage in local text files
        self.login("admin", "pass123")

        # Navigate to the Listing Page
        self.driver.find_element(By.LINK_TEXT, 'Add New Item').click()
        time.sleep(1)  # Wait for the listing page to load

        # Fill out the new item form
        self.driver.find_element(By.NAME, 'name').send_keys("Stored Vintage Item")
        self.driver.find_element(By.NAME, 'description').send_keys("Stored item description.")
        self.driver.find_element(By.NAME, 'price').send_keys("59.99")
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        time.sleep(1)  # Wait for the home page to load

        # Verify that the new item is stored in the local text file
        with open('items.txt', 'r') as file:
            self.assertIn("Stored Vintage Item", file.read())

if __name__ == '__main__':
    unittest.main()
