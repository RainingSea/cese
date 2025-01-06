import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineVintageMarket(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8178/')  # Access the login page

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
        self.login("user1", "password1")

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
        self.login("user1", "password1")

        # Verify that the Home Page shows items
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No vintage items found.")

    def test_search_for_specific_vintage_item(self):
        # Functionalities 4: Test searching for a specific vintage item by name
        self.login("user1", "password1")

        # Search for a specific item
        item_name = "Vintage Clock"
        item_link = self.driver.find_element(By.LINK_TEXT, item_name)
        self.assertIsNotNone(item_link, f"Item {item_name} not found.")

    def test_view_details_of_selected_item(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("user1", "password1")

        # Click on an item to view details
        item_name = "Vintage Clock"
        self.driver.find_element(By.LINK_TEXT, item_name).click()
        time.sleep(1)  # Wait for the item details page to load

        # Verify the item details page
        self.assertIn(item_name, self.driver.title)

    def test_create_new_listing(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.login("user1", "password1")

        # Navigate to Listing Page
        self.driver.find_element(By.LINK_TEXT, 'Create Listing').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the new listing form
        self.driver.find_element(By.NAME, 'name').send_keys("New Vintage Item")
        self.driver.find_element(By.NAME, 'description').send_keys("Description of the new vintage item.")
        self.driver.find_element(By.NAME, 'price').send_keys("100.00")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()
        time.sleep(1)  # Wait for the listing to be submitted

        # Verify that the new item is listed on the Home Page
        self.assertIn("New Vintage Item", self.driver.page_source)

    def test_submit_item_listing(self):
        # Functionalities 7: Test submitting an item listing
        self.login("user1", "password1")

        # Navigate to Listing Page
        self.driver.find_element(By.LINK_TEXT, 'Create Listing').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the new listing form
        self.driver.find_element(By.NAME, 'name').send_keys("Another Vintage Item")
        self.driver.find_element(By.NAME, 'description').send_keys("Description of another vintage item.")
        self.driver.find_element(By.NAME, 'price').send_keys("200.00")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()
        time.sleep(1)  # Wait for the listing to be submitted

        # Verify that the new item is listed on the Home Page
        self.assertIn("Another Vintage Item", self.driver.page_source)

    def test_view_detailed_information_about_vintage_item(self):
        # Functionalities 8: Test viewing detailed information about a vintage item
        self.login("user1", "password1")

        # Click on an item to view details
        item_name = "Vintage Clock"
        self.driver.find_element(By.LINK_TEXT, item_name).click()
        time.sleep(1)  # Wait for the item details page to load

        # Verify the item details page
        self.assertIn(item_name, self.driver.title)

    def test_navigate_back_to_home_from_item_details(self):
        # Functionalities 9: Test navigating back to Home Page from Item Details Page
        self.login("user1", "password1")

        # Click on an item to view details
        item_name = "Vintage Clock"
        self.driver.find_element(By.LINK_TEXT, item_name).click()
        time.sleep(1)  # Wait for the item details page to load

        # Navigate back to Home Page
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the Home Page to load

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_data_storage_in_local_text_files(self):
        # Functionalities 10: Test data storage in local text files
        self.login("user1", "password1")

        # Navigate to Listing Page
        self.driver.find_element(By.LINK_TEXT, 'Create Listing').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the new listing form
        item_name = "Stored Vintage Item"
        self.driver.find_element(By.NAME, 'name').send_keys(item_name)
        self.driver.find_element(By.NAME, 'description').send_keys("Description of stored vintage item.")
        self.driver.find_element(By.NAME, 'price').send_keys("300.00")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()
        time.sleep(1)  # Wait for the listing to be submitted

        # Verify that the new item is listed on the Home Page
        self.assertIn(item_name, self.driver.page_source)

        # Check if the item is stored in the text file
        with open('items.txt', 'r') as file:
            content = file.read()
            self.assertIn(item_name, content)

if __name__ == '__main__':
    unittest.main()
