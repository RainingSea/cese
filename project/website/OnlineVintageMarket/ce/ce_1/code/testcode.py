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
        self.driver.get('http://localhost:8179')

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
        # Functionalities 3: Test viewing available vintage items
        self.login("admin", "adminpass")

        # Verify that the Home Page shows items
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No vintage items found.")

    def test_search_vintage_item_by_name(self):
        # Functionalities 4: Test searching for a specific vintage item by name
        self.login("admin", "adminpass")

        # Search for an item
        self.driver.find_element(By.NAME, 'search').send_keys("Vintage Clock")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results

        # Verify that the search result contains the item
        self.assertIn("Vintage Clock", self.driver.page_source)

    def test_view_details_of_selected_item(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("admin", "adminpass")

        # Click on an item to view details
        self.driver.find_element(By.LINK_TEXT, 'Vintage Clock').click()
        time.sleep(1)  # Wait for the item details page to load

        # Verify that the item details page shows correct information
        self.assertIn("Vintage Clock", self.driver.page_source)
        self.assertIn("A beautiful vintage clock from the 1950s", self.driver.page_source)
        self.assertIn("150.0$", self.driver.page_source)

    def test_create_new_listing(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.fail("Not implemented")

    def test_submit_item_listing(self):
        # Functionalities 7: Test submitting an item listing
        self.fail("Not implemented")

    def test_view_detailed_information_about_vintage_item(self):
        # Functionalities 8: Test viewing detailed information about a vintage item
        self.login("admin", "adminpass")

        # Click on an item to view details
        self.driver.find_element(By.LINK_TEXT, 'Vintage Clock').click()
        time.sleep(1)  # Wait for the item details page to load

        # Verify that the item details page shows correct information
        self.assertIn("Vintage Clock", self.driver.page_source)
        self.assertIn("A beautiful vintage clock from the 1950s", self.driver.page_source)
        self.assertIn("150.0$", self.driver.page_source)

    def test_navigate_back_to_home_page(self):
        # Functionalities 9: Test navigating back to home page from item details page
        self.login("admin", "adminpass")

        # Click on an item to view details
        self.driver.find_element(By.LINK_TEXT, 'Vintage Clock').click()
        time.sleep(1)  # Wait for the item details page to load

        # Click the back link to return to home page
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the home page to load

        # Verify that the Home Page has loaded
        self.assertIn("Available Vintage Items", self.driver.page_source)

    def test_data_storage_in_local_text_files(self):
        # Functionalities 10: Test data storage in local text files
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
