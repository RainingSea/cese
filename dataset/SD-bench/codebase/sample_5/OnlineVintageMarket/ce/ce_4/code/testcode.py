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
        self.driver.get('http://localhost:8469/') 

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

    def test_view_available_vintage_items(self):
        # Functionalities 3: Test viewing available vintage items after logging in
        self.login("admin", "admin123")

        # Verify that the Home Page shows items
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No vintage items found.")

    def test_search_vintage_item_by_name(self):
        # Functionalities 4: Test searching for a specific vintage item by name
        self.login("admin", "admin123")

        # Perform search
        self.driver.find_element(By.NAME, 'search').send_keys("Vintage Clock")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results

        # Verify that the search results contain the item
        self.assertIn("Vintage Clock", self.driver.page_source)

    def test_view_item_details(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("admin", "admin123")

        # Click on the first item link
        self.driver.find_element(By.LINK_TEXT, 'Vintage Clock').click()
        time.sleep(1)  # Wait for the item details page to load

        # Verify that the Item Details Page shows correct information
        self.assertIn("Vintage Clock", self.driver.page_source)
        self.assertIn("A beautiful vintage clock from the 1950s", self.driver.page_source)
        self.assertIn("49.99", self.driver.page_source)

    def test_create_new_listing(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.login("admin", "admin123")

        # Navigate to Listing Page
        self.driver.find_element(By.LINK_TEXT, 'List a new item').click()
        time.sleep(1)  # Wait for the listing page to load

        # Fill out the new listing form
        self.driver.find_element(By.NAME, 'name').send_keys("New Vintage Item")
        self.driver.find_element(By.NAME, 'description').send_keys("A description of the new vintage item.")
        self.driver.find_element(By.NAME, 'price').send_keys("99.99")
        self.driver.find_element(By.XPATH, '//button[text()="List Item"]').click()
        time.sleep(1)  # Wait for the listing to be processed

        # Verify that the user is redirected to the Home Page
        self.assertIn("Home", self.driver.title)

    def test_submit_item_listing(self):
        # Functionalities 7: Test submitting a valid item listing
        self.login("admin", "admin123")

        # Navigate to Listing Page
        self.driver.find_element(By.LINK_TEXT, 'List a new item').click()
        time.sleep(1)  # Wait for the listing page to load

        # Fill out the new listing form
        self.driver.find_element(By.NAME, 'name').send_keys("Another Vintage Item")
        self.driver.find_element(By.NAME, 'description').send_keys("Another description.")
        self.driver.find_element(By.NAME, 'price').send_keys("79.99")
        self.driver.find_element(By.XPATH, '//button[text()="List Item"]').click()
        time.sleep(1)  # Wait for the listing to be processed

        # Verify that the user is redirected to the Home Page
        self.assertIn("Home", self.driver.title)

    def test_view_detailed_information(self):
        # Functionalities 8: Test viewing detailed information about a vintage item
        self.login("admin", "admin123")

        # Click on the first item link
        self.driver.find_element(By.LINK_TEXT, 'Vintage Clock').click()
        time.sleep(1)  # Wait for the item details page to load

        # Verify that the Item Details Page shows correct information
        self.assertIn("Vintage Clock", self.driver.page_source)
        self.assertIn("A beautiful vintage clock from the 1950s", self.driver.page_source)
        self.assertIn("49.99", self.driver.page_source)

    def test_navigate_back_to_home(self):
        # Functionalities 9: Test navigating back to Home Page from Item Details Page
        self.login("admin", "admin123")

        # Click on the first item link
        self.driver.find_element(By.LINK_TEXT, 'Vintage Clock').click()
        time.sleep(1)  # Wait for the item details page to load

        # Click on the "Back to Home" link
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the home page to load

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_data_storage(self):
        # Functionalities 10: Test data storage in local text files
        self.fail("not implemented")

if __name__ == '__main__':
    unittest.main()
