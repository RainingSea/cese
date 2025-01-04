import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineVintageMarket(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8136')

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
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Login", self.driver.title)

    def test_view_available_vintage_items(self):
        # Functionalities 3: Test viewing available vintage items
        self.login("admin", "pass123")
        items = self.driver.find_elements(By.CSS_SELECTOR, '#item-list li')
        self.assertGreater(len(items), 0, "No vintage items found.")

    def test_search_vintage_item_by_name(self):
        # Functionalities 4: Test searching for a specific vintage item by name
        self.login("admin", "pass123")
        search_box = self.driver.find_element(By.ID, 'search')
        search_box.send_keys("Vintage Clock")
        time.sleep(1)  # Wait for the search to filter items

        items = self.driver.find_elements(By.CSS_SELECTOR, '#item-list li')
        self.assertTrue(any("Vintage Clock" in item.text for item in items), "Item not found in search results.")

    def test_view_item_details(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Vintage Clock').click()
        time.sleep(1)  # Wait for the item details page to load

        self.assertIn("Item Details", self.driver.title)
        self.assertIn("Vintage Clock", self.driver.page_source)

    def test_create_new_listing(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Listing').click()
        time.sleep(1)  # Wait for the listing page to load

        self.driver.find_element(By.NAME, 'name').send_keys("New Vintage Item")
        self.driver.find_element(By.NAME, 'description').send_keys("A description of the new vintage item.")
        self.driver.find_element(By.NAME, 'price').send_keys("100.00")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()
        time.sleep(1)  # Wait for the listing to be submitted

        self.assertIn("Home", self.driver.title)

    def test_submit_item_listing(self):
        # Functionalities 7: Test submitting an item listing
        self.fail("Not implemented")

    def test_view_detailed_information_about_item(self):
        # Functionalities 8: Test viewing detailed information about a vintage item
        self.fail("Not implemented")

    def test_navigate_back_to_home_from_item_details(self):
        # Functionalities 9: Test navigating back to home page from item details page
        self.fail("Not implemented")

    def test_data_storage_in_local_text_files(self):
        # Functionalities 10: Test data storage in local text files
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
