import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestOnlineVintageMarket(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8380/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)  # Verify redirection to Home Page

    def test_registration(self):
        # Functionalities 2: User Registration
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

    def test_view_available_items(self):
        # Functionalities 3: View Available Vintage Items
        self.login("admin", "admin123")
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No items found on the Home Page.")

    def test_view_item_details(self):
        # Functionalities 5: View Details of a Selected Item
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Item Details").click()  # Click on the first item details link
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Item Details", self.driver.title)  # Verify redirection to Item Details Page

    def test_create_new_listing(self):
        # Functionalities 6: Create a New Listing for Vintage Items
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'List a New Item').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the new item listing form
        self.driver.find_element(By.NAME, 'name').send_keys("Vintage Lamp")
        self.driver.find_element(By.NAME, 'description').send_keys("A beautiful vintage lamp.")
        self.driver.find_element(By.NAME, 'price').send_keys("45.00")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the item is listed on the Home Page
        self.assertIn("Vintage Lamp", self.driver.page_source)

    def test_view_item_details_specific(self):
        # Functionalities 8: View Detailed Information About a Vintage Item
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Item Details").click()  # Click on the first item details link
        time.sleep(1)  # Wait for the next page to load
        details = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertIn("Name:", details)  # Verify that item details are displayed

    def test_navigate_back_to_home(self):
        # Functionalities 9: Navigate Back to Home Page from Item Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Item Details").click()  # Click on the first item details link
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.LINK_TEXT, "Back to Home").click()  # Click back to home
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Home", self.driver.title)  # Verify redirection to Home Page

    def test_data_storage(self):
        # Functionalities 10: Data Storage in Local Text Files
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'List a New Item').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the new item listing form
        self.driver.find_element(By.NAME, 'name').send_keys("Vintage Chair")
        self.driver.find_element(By.NAME, 'description').send_keys("A classic vintage chair.")
        self.driver.find_element(By.NAME, 'price').send_keys("75.00")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the item is saved in the local text file
        with open('items.txt', 'r') as file:
            items = file.readlines()
            self.assertIn("Vintage Chair|A classic vintage chair.|75.00\n", items)

if __name__ == '__main__':
    unittest.main()
