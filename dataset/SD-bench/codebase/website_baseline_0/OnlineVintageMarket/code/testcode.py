import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineVintageMarket(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8545/')

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
        self.login("admin", "admin123")

        # Perform a search
        search_box = self.driver.find_element(By.NAME, 'query')
        search_box.send_keys("Vintage Clock")
        search_box.submit()
        time.sleep(1)  # Wait for the search results to load

        # Verify that the search results contain the specific item
        self.assertIn("Vintage Clock", self.driver.page_source)

    def test_view_item_details(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("admin", "admin123")

        # Click on an item to view its details
        self.driver.find_element(By.LINK_TEXT, 'Vintage Clock').click()
        time.sleep(1)  # Wait for the item details page to load

        # Verify that the Item Details Page displays the correct information
        self.assertIn("Vintage Clock", self.driver.page_source)
        self.assertIn("A beautiful vintage clock from the 1950s", self.driver.page_source)
        self.assertIn("$49.99", self.driver.page_source)

    def test_create_new_listing(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.login("admin", "admin123")

        # Navigate to the Listing Page
        self.driver.find_element(By.LINK_TEXT, 'List a New Item').click()
        time.sleep(1)  # Wait for the listing page to load

        # Fill out the new listing form
        self.driver.find_element(By.NAME, 'name').send_keys("Vintage Radio")
        self.driver.find_element(By.NAME, 'description').send_keys("A classic vintage radio from the 1960s")
        self.driver.find_element(By.NAME, 'price').send_keys("79.99")
        self.driver.find_element(By.XPATH, '//button[text()="List Item"]').click()
        time.sleep(1)  # Wait for the listing to be processed

        # Verify that the new item is displayed on the Home Page
        self.assertIn("Vintage Radio", self.driver.page_source)

    def test_submit_item_listing(self):
        # Functionalities 7: Test submitting a valid item listing
        self.login("admin", "admin123")

        # Navigate to the Listing Page
        self.driver.find_element(By.LINK_TEXT, 'List a New Item').click()
        time.sleep(1)  # Wait for the listing page to load

        # Fill out the new listing form
        self.driver.find_element(By.NAME, 'name').send_keys("Vintage Lamp")
        self.driver.find_element(By.NAME, 'description').send_keys("A beautiful vintage lamp from the 1970s")
        self.driver.find_element(By.NAME, 'price').send_keys("59.99")
        self.driver.find_element(By.XPATH, '//button[text()="List Item"]').click()
        time.sleep(1)  # Wait for the listing to be processed

        # Verify that the new item is displayed on the Home Page
        self.assertIn("Vintage Lamp", self.driver.page_source)

    def test_view_detailed_information(self):
        # Functionalities 8: Test viewing detailed information about a vintage item
        self.login("admin", "admin123")

        # Click on an item to view its details
        self.driver.find_element(By.LINK_TEXT, 'Antique Vase').click()
        time.sleep(1)  # Wait for the item details page to load

        # Verify that the Item Details Page displays the correct information
        self.assertIn("Antique Vase", self.driver.page_source)
        self.assertIn("An exquisite vase from the 19th century", self.driver.page_source)
        self.assertIn("$89.99", self.driver.page_source)

    def test_navigate_back_to_home(self):
        # Functionalities 9: Test navigating back to the Home Page from Item Details Page
        self.login("admin", "admin123")

        # Click on an item to view its details
        self.driver.find_element(By.LINK_TEXT, 'Antique Vase').click()
        time.sleep(1)  # Wait for the item details page to load

        # Click the Home link to navigate back
        self.driver.find_element(By.LINK_TEXT, 'Home').click()
        time.sleep(1)  # Wait for the Home Page to load

        # Verify that the Home Page is displayed
        self.assertIn("Available Vintage Items", self.driver.page_source)

    def test_data_storage_in_local_files(self):
        # Functionalities 10: Test data storage in local text files
        self.login("admin", "admin123")

        # Navigate to the Listing Page
        self.driver.find_element(By.LINK_TEXT, 'List a New Item').click()
        time.sleep(1)  # Wait for the listing page to load

        # Fill out the new listing form
        self.driver.find_element(By.NAME, 'name').send_keys("Vintage Camera")
        self.driver.find_element(By.NAME, 'description').send_keys("A classic vintage camera from the 1980s")
        self.driver.find_element(By.NAME, 'price').send_keys("99.99")
        self.driver.find_element(By.XPATH, '//button[text()="List Item"]').click()
        time.sleep(1)  # Wait for the listing to be processed

        # Verify that the new item is saved in the local text file
        with open('items.txt', 'r') as file:
            items = file.read()
            self.assertIn("Vintage Camera", items)

if __name__ == '__main__':
    unittest.main()
