import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOnlineVintageMarket(unittest.TestCase):

    def setUp(self):
        # Start the main application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace 5000 with the actual port from main.py

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
        self.assertIn("Home", self.driver.title)  # Check if redirected to Home Page

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
        # Functionalities 3: Test viewing available vintage items
        self.login("admin", "admin123")
        items_list = self.driver.find_element(By.ID, 'items-list').text
        self.assertIn("Vintage Clock", items_list)  # Check if an item is listed

    def test_search_item(self):
        # Functionalities 4: Test searching for a specific vintage item
        self.login("admin", "admin123")
        search_box = self.driver.find_element(By.ID, 'search')
        search_box.send_keys("Vintage Clock")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that the search results show the specific item
        self.assertIn("Vintage Clock", self.driver.page_source)

    def test_view_item_details(self):
        # Functionalities 5: Test viewing details of a selected item
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Vintage Clock").click()  # Assuming item name is a link

        # Verify that the Item Details Page shows the correct information
        self.assertIn("Vintage Clock", self.driver.page_source)
        self.assertIn("An antique clock from the 1950s", self.driver.page_source)

    def test_create_new_listing(self):
        # Functionalities 6: Test creating a new listing for vintage items
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit a new listing').click()

        # Fill out the new listing form
        self.driver.find_element(By.NAME, 'name').send_keys("New Vintage Item")
        self.driver.find_element(By.NAME, 'description').send_keys("A description of the new item.")
        self.driver.find_element(By.NAME, 'price').send_keys("100.00")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()

        # Verify that the new item is listed
        items_list = self.driver.find_element(By.ID, 'items-list').text
        self.assertIn("New Vintage Item", items_list)

    def test_submit_item_listing(self):
        # Functionalities 7: Test submitting an item listing
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit a new listing').click()

        # Fill out the new listing form
        self.driver.find_element(By.NAME, 'name').send_keys("Another Vintage Item")
        self.driver.find_element(By.NAME, 'description').send_keys("Another description.")
        self.driver.find_element(By.NAME, 'price').send_keys("150.00")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()

        # Verify confirmation message (assuming it redirects back to home)
        self.assertIn("Available Vintage Items", self.driver.page_source)

    def test_view_item_details_page(self):
        # Functionalities 8: Test viewing detailed information about a vintage item
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Vintage Clock").click()

        # Verify that the Item Details Page displays the correct information
        self.assertIn("Name: Vintage Clock", self.driver.page_source)

    def test_navigate_back_to_home(self):
        # Functionalities 9: Test navigating back to Home Page from Item Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Vintage Clock").click()
        self.driver.find_element(By.LINK_TEXT, "Back to Home").click()

        # Verify that the user is redirected back to the Home Page
        self.assertIn("Available Vintage Items", self.driver.page_source)

    def test_data_storage(self):
        # Functionalities 10: Test data storage in local text files
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit a new listing').click()
        self.driver.find_element(By.NAME, 'name').send_keys("Test Item")
        self.driver.find_element(By.NAME, 'description').send_keys("Test description.")
        self.driver.find_element(By.NAME, 'price').send_keys("200.00")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Listing"]').click()

        # Check if the item is saved in items.txt (this part would require file access)
        with open('items.txt', 'r') as file:
            items = file.read()
            self.assertIn("Test Item", items)

if __name__ == '__main__':
    unittest.main()
