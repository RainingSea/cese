import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOnlineVintageMarket(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8212/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)

    def test_registration(self):
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
        
        # Verify that the Home Page shows items
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No vintage items found.")

    def test_view_item_details(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("admin", "admin123")
        
        # Click on the first item's details link
        self.driver.find_element(By.XPATH, '//li/a').click()
        
        # Verify that the Item Details Page is displayed
        self.assertIn("Item Details", self.driver.title)

    def test_create_new_listing(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.login("admin", "admin123")
        
        # Navigate to the Listing Page
        self.driver.find_element(By.LINK_TEXT, 'Submit Listing').click()
        
        # Fill out the new item listing form
        self.driver.find_element(By.NAME, 'name').send_keys("Vintage Lamp")
        self.driver.find_element(By.NAME, 'description').send_keys("A beautiful vintage lamp.")
        self.driver.find_element(By.NAME, 'price').send_keys("59.99")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()

        # Verify that the item is listed on the Home Page
        self.assertIn("Vintage Lamp", self.driver.page_source)

    def test_navigate_back_to_home(self):
        # Functionalities 9: Test navigating back to Home Page from Item Details Page
        self.login("admin", "admin123")
        
        # Click on the first item's details link
        self.driver.find_element(By.XPATH, '//li/a').click()
        
        # Click the Back button
        self.driver.find_element(By.LINK_TEXT, 'Back').click()
        
        # Verify that the user is redirected back to the Home Page
        self.assertIn("Vintage Items", self.driver.title)

    def test_data_storage(self):
        # Functionalities 10: Test data storage in local text files
        self.login("admin", "admin123")
        
        # Create a new listing
        self.driver.find_element(By.LINK_TEXT, 'Submit Listing').click()
        self.driver.find_element(By.NAME, 'name').send_keys("Vintage Chair")
        self.driver.find_element(By.NAME, 'description').send_keys("A classic vintage chair.")
        self.driver.find_element(By.NAME, 'price').send_keys("89.99")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()

        # Verify that the new item details are saved in items.txt
        with open('items.txt', 'r') as f:
            items = f.readlines()
            self.assertIn("Vintage Chair|A classic vintage chair.|89.99\n", items)

if __name__ == '__main__':
    unittest.main()
