import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineVintageMarket(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        # Close the web driver and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:5000')
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)

    def test_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.get('http://localhost:5000/register')
        time.sleep(1)  # Wait for the registration page to load

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
        # Functionalities 3: Test viewing available vintage items after logging in
        self.login("admin", "admin123")
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No vintage items found.")

    def test_view_item_details(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Vintage Clock").click()
        time.sleep(1)  # Wait for the item details page to load

        self.assertIn("Vintage Clock", self.driver.title)
        self.assertIn("A beautiful vintage clock from the 1950s", self.driver.page_source)

    def test_create_new_listing(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Listing').click()
        time.sleep(1)  # Wait for the listing page to load

        # Fill out the new item form
        self.driver.find_element(By.NAME, 'name').send_keys("New Vintage Item")
        self.driver.find_element(By.NAME, 'description').send_keys("Description of new vintage item.")
        self.driver.find_element(By.NAME, 'price').send_keys("99.99")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()
        time.sleep(1)  # Wait for the submission to complete

        # Verify that the new item is displayed on the Home Page
        self.assertIn("New Vintage Item", self.driver.page_source)

    def test_navigate_back_to_home(self):
        # Functionalities 9: Test navigating back to Home Page from Item Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Vintage Clock").click()
        time.sleep(1)  # Wait for the item details page to load

        self.driver.find_element(By.LINK_TEXT, "Back").click()
        time.sleep(1)  # Wait for the Home Page to load

        self.assertIn("Home", self.driver.title)

    def test_data_storage(self):
        # Functionalities 10: Test data storage in local text files
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Listing').click()
        time.sleep(1)  # Wait for the listing page to load

        # Fill out the new item form
        self.driver.find_element(By.NAME, 'name').send_keys("Test Item")
        self.driver.find_element(By.NAME, 'description').send_keys("Test description.")
        self.driver.find_element(By.NAME, 'price').send_keys("29.99")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()
        time.sleep(1)  # Wait for the submission to complete

        # Verify that the new item is saved in the items.txt file
        with open('items.txt', 'r') as f:
            items = f.readlines()
            self.assertIn("Test Item|Test description.|29.99\n", items)

if __name__ == '__main__':
    unittest.main()
