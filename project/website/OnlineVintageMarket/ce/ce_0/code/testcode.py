import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOnlineVintageMarket(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8210/') 

    def tearDown(self):
        # Close the web driver session
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
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_available_items(self):
        # Functionalities 3: Test viewing available vintage items after logging in
        self.login("admin", "admin123")
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No items found.")

    def test_view_item_details(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Item Details').click()

        # Verify that the Item Details Page shows the correct item information
        self.assertIn("Item Details", self.driver.title)

    def test_create_new_listing(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'List a new item').click()

        # Fill out the new item form
        self.driver.find_element(By.NAME, 'name').send_keys("Vintage Camera")
        self.driver.find_element(By.NAME, 'description').send_keys("A classic camera from the 1970s.")
        self.driver.find_element(By.NAME, 'price').send_keys("250.00")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()

        # Verify that the item is listed on the Home Page
        self.assertIn("Vintage Camera", self.driver.page_source)

    def test_navigate_back_to_home(self):
        # Functionalities 9: Test navigating back to Home Page from Item Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Item Details').click()
        self.driver.find_element(By.LINK_TEXT, 'Back').click()

        # Verify that the user is redirected back to the Home Page
        self.assertIn("Home", self.driver.title)

    def test_data_storage(self):
        # Functionalities 10: Test data storage in local text files
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'List a new item').click()
        self.driver.find_element(By.NAME, 'name').send_keys("Vintage Watch")
        self.driver.find_element(By.NAME, 'description').send_keys("A stylish vintage watch.")
        self.driver.find_element(By.NAME, 'price').send_keys("150.00")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()

        # Verify that the new item details are saved to the local text file
        with open('items.txt', 'r') as file:
            contents = file.read()
            self.assertIn("Vintage Watch", contents)

if __name__ == '__main__':
    unittest.main()
