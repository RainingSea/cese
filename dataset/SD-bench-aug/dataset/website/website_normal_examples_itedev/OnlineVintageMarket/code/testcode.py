import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineVintageMarket(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

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
        self.login("user1", "password1")

        # Verify that the Home Page shows items
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No vintage items found.")

    def test_search_vintage_item_by_name(self):
        # Functionalities 4: Test searching for a specific vintage item by name
        self.fail("not implemented")

    def test_view_details_of_selected_item(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("user1", "password1")

        # Click on the first item's details link
        self.driver.find_element(By.LINK_TEXT, 'Item Details').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Item Details Page has loaded
        self.assertIn("Item Details", self.driver.title)

    def test_create_new_listing(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.login("user1", "password1")

        # Navigate to the Listing Page
        self.driver.find_element(By.LINK_TEXT, 'Create Listing').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the new listing form
        self.driver.find_element(By.NAME, 'name').send_keys("Vintage Lamp")
        self.driver.find_element(By.NAME, 'description').send_keys("A beautiful vintage lamp.")
        self.driver.find_element(By.NAME, 'price').send_keys("120.00")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Home Page
        self.assertIn("Home", self.driver.title)

    def test_submit_item_listing(self):
        # Functionalities 7: Test submitting an item listing
        self.fail("not implemented")

    def test_view_detailed_information_about_vintage_item(self):
        # Functionalities 8: Test viewing detailed information about a vintage item
        self.fail("not implemented")

    def test_navigate_back_to_home_page(self):
        # Functionalities 9: Test navigating back to the Home Page from Item Details Page
        self.login("user1", "password1")

        # Click on the first item's details link
        self.driver.find_element(By.LINK_TEXT, 'Item Details').click()
        time.sleep(1)  # Wait for the next page to load

        # Click the Back link
        self.driver.find_element(By.LINK_TEXT, 'Back').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected back to the Home Page
        self.assertIn("Home", self.driver.title)

    def test_data_storage_in_local_text_files(self):
        # Functionalities 10: Test data storage in local text files
        self.fail("not implemented")

if __name__ == '__main__':
    unittest.main()
