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
        self.driver.get('http://localhost:8466/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and stop the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Login", self.driver.title)

    def test_view_available_vintage_items(self):
        # Functionalities 3: View Available Vintage Items
        self.login("admin", "admin123")
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No vintage items found.")

    def test_search_vintage_item_by_name(self):
        # Functionalities 4: Search for a Specific Vintage Item by Name
        self.login("admin", "admin123")
        item_name = "Vintage Clock"
        item_link = self.driver.find_element(By.LINK_TEXT, item_name)
        self.assertIsNotNone(item_link, f"Item '{item_name}' not found.")

    def test_view_details_of_selected_item(self):
        # Functionalities 5: View Details of a Selected Item
        self.login("admin", "admin123")
        item_name = "Vintage Clock"
        self.driver.find_element(By.LINK_TEXT, item_name).click()
        time.sleep(1)  # Wait for the item details page to load
        self.assertIn(item_name, self.driver.page_source)

    def test_create_new_listing(self):
        # Functionalities 6: Create a New Listing for Vintage Items
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create Listing').click()
        time.sleep(1)  # Wait for the listing page to load

        item_name = "New Vintage Item"
        item_description = "A description of the new vintage item."
        item_price = "100"

        self.driver.find_element(By.NAME, 'name').send_keys(item_name)
        self.driver.find_element(By.NAME, 'description').send_keys(item_description)
        self.driver.find_element(By.NAME, 'price').send_keys(item_price)
        self.driver.find_element(By.XPATH, '//button[text()="Create Listing"]').click()
        time.sleep(1)  # Wait for the home page to load

        self.assertIn(item_name, self.driver.page_source)

    def test_submit_item_listing(self):
        # Functionalities 7: Submit Item Listing
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create Listing').click()
        time.sleep(1)  # Wait for the listing page to load

        item_name = "Another Vintage Item"
        item_description = "Description for another vintage item."
        item_price = "150"

        self.driver.find_element(By.NAME, 'name').send_keys(item_name)
        self.driver.find_element(By.NAME, 'description').send_keys(item_description)
        self.driver.find_element(By.NAME, 'price').send_keys(item_price)
        self.driver.find_element(By.XPATH, '//button[text()="Create Listing"]').click()
        time.sleep(1)  # Wait for the home page to load

        self.assertIn(item_name, self.driver.page_source)

    def test_view_detailed_information_about_vintage_item(self):
        # Functionalities 8: View Detailed Information About a Vintage Item
        self.login("admin", "admin123")
        item_name = "Vintage Clock"
        self.driver.find_element(By.LINK_TEXT, item_name).click()
        time.sleep(1)  # Wait for the item details page to load
        self.assertIn(item_name, self.driver.page_source)

    def test_navigate_back_to_home_page_from_item_details(self):
        # Functionalities 9: Navigate Back to Home Page from Item Details Page
        self.login("admin", "admin123")
        item_name = "Vintage Clock"
        self.driver.find_element(By.LINK_TEXT, item_name).click()
        time.sleep(1)  # Wait for the item details page to load
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the home page to load
        self.assertIn("Available Vintage Items", self.driver.page_source)

    def test_data_storage_in_local_text_files(self):
        # Functionalities 10: Data Storage in Local Text Files
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
