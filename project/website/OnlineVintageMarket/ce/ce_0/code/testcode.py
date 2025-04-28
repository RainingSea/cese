import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOnlineVintageMarketApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8378/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)  # Expect to be redirected to Home Page

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_available_items(self):
        # Functionalities 3: Test viewing available vintage items after logging in
        self.login("admin", "admin123")
        self.assertIn("Available Vintage Items", self.driver.page_source)  # Check if items are displayed

    def test_view_item_details(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Antique Vase').click()  # Click on the item
        self.assertIn("Item Details", self.driver.title)  # Check if redirected to item details page

    def test_create_new_listing(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'List a new item').click()

        # Fill out the new item form
        self.driver.find_element(By.NAME, 'item_name').send_keys("Vintage Lamp")
        self.driver.find_element(By.NAME, 'description').send_keys("A beautiful vintage lamp.")
        self.driver.find_element(By.NAME, 'price').send_keys("75.00")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()

        # Verify that the item is listed
        self.assertIn("Vintage Lamp", self.driver.page_source)

    def test_view_item_details_from_home(self):
        # Functionalities 8: Test viewing detailed information about a vintage item
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Antique Vase').click()  # Click on the item
        details = self.driver.find_element(By.TAG_NAME, 'p').text  # Get the details text
        self.assertIn("Antique Vase", details)  # Check if the item name is in the details

    def test_navigate_back_to_home(self):
        # Functionalities 9: Test navigating back to Home Page from Item Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Antique Vase').click()  # Click on the item
        self.driver.find_element(By.LINK_TEXT, 'Back').click()  # Click the back button
        self.assertIn("Available Vintage Items", self.driver.page_source)  # Check if back to home

    def test_data_storage(self):
        # Functionalities 10: Test data storage in local text files
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'List a new item').click()

        # Fill out the new item form
        self.driver.find_element(By.NAME, 'item_name').send_keys("Vintage Chair")
        self.driver.find_element(By.NAME, 'description').send_keys("A stylish vintage chair.")
        self.driver.find_element(By.NAME, 'price').send_keys("120.00")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()

        # Verify that the item is listed
        self.assertIn("Vintage Chair", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
