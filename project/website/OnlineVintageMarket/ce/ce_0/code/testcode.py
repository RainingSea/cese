import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os
import json

class TestOnlineVintageMarket(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8113/')
        self.driver.implicitly_wait(2)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)

    def test_1_user_login(self):
        """Functionalities 1: User Login with valid credentials"""
        self.login("admin", "admin123")
        self.assertIn("Welcome", self.driver.page_source)
        self.assertEqual(self.driver.current_url, "http://localhost:8113/home")

    def test_2_user_registration(self):
        """Functionalities 2: User Registration with new credentials"""
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        
        username = f"testuser{int(time.time())}"
        password = "testpass123"
        email = f"{username}@example.com"
        
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.NAME, 'email').send_keys(email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        self.assertEqual(self.driver.current_url, "http://localhost:8113/")
        self.assertIn("Login", self.driver.title)

    def test_3_view_available_items(self):
        """Functionalities 3: View Available Vintage Items"""
        self.login("admin", "admin123")
        items = self.driver.find_elements(By.CSS_SELECTOR, 'div[style*="border: 1px solid #ccc"]')
        self.assertGreater(len(items), 0)

    def test_4_search_items_by_name(self):
        """Functionalities 4: Search for a Specific Vintage Item by Name"""
        self.login("admin", "admin123")
        search_box = self.driver.find_element(By.NAME, 'query')
        search_box.send_keys("Vintage Lamp")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        items = self.driver.find_elements(By.CSS_SELECTOR, 'div[style*="border: 1px solid #ccc"]')
        self.assertEqual(len(items), 1)
        self.assertIn("Vintage Lamp", self.driver.page_source)

    def test_5_view_item_details(self):
        """Functionalities 5: View Details of a Selected Item"""
        self.login("admin", "admin123")
        item_link = self.driver.find_element(By.LINK_TEXT, "Details")
        item_link.click()
        
        self.assertIn("Vintage Lamp", self.driver.page_source)
        self.assertIn("Antique brass lamp", self.driver.page_source)
        self.assertIn("$45.99", self.driver.page_source)

    def test_6_create_new_listing(self):
        """Functionalities 6: Create a New Listing for Vintage Items"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add New Listing').click()
        
        item_name = f"Test Item {int(time.time())}"
        self.driver.find_element(By.NAME, 'name').send_keys(item_name)
        self.driver.find_element(By.NAME, 'description').send_keys("Test description")
        self.driver.find_element(By.NAME, 'price').send_keys("99.99")
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        
        self.assertEqual(self.driver.current_url, "http://localhost:8113/home")
        self.assertIn(item_name, self.driver.page_source)

    def test_7_submit_item_listing(self):
        """Functionalities 7: Submit Item Listing"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add New Listing').click()
        
        item_name = f"Test Submit {int(time.time())}"
        self.driver.find_element(By.NAME, 'name').send_keys(item_name)
        self.driver.find_element(By.NAME, 'description').send_keys("Test submit description")
        self.driver.find_element(By.NAME, 'price').send_keys("49.99")
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        
        self.assertEqual(self.driver.current_url, "http://localhost:8113/home")
        self.assertIn(item_name, self.driver.page_source)

    def test_8_view_detailed_information(self):
        """Functionalities 8: View Detailed Information About a Vintage Item"""
        self.login("admin", "admin123")
        item_link = self.driver.find_element(By.LINK_TEXT, "Details")
        item_link.click()
        
        self.assertIn("Vintage Lamp", self.driver.find_element(By.TAG_NAME, 'h1').text)
        self.assertIn("Antique brass lamp", self.driver.page_source)
        self.assertIn("$45.99", self.driver.page_source)
        self.assertIn("admin", self.driver.page_source)

    def test_9_navigate_back_to_home(self):
        """Functionalities 9: Navigate Back to Home Page from Item Details Page"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Details').click()
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        
        self.assertEqual(self.driver.current_url, "http://localhost:8113/home")
        self.assertIn("Welcome", self.driver.page_source)

    def test_10_data_storage(self):
        """Functionalities 10: Data Storage in Local Text Files"""
        # First, check initial item count
        initial_item_count = len(self.driver.find_elements(By.CSS_SELECTOR, 'div[style*="border: 1px solid #ccc"]'))
        
        # Create a new listing
        self.driver.find_element(By.LINK_TEXT, 'Add New Listing').click()
        
        item_name = f"Storage Test {int(time.time())}"
        self.driver.find_element(By.NAME, 'name').send_keys(item_name)
        self.driver.find_element(By.NAME, 'description').send_keys("Storage test description")
        self.driver.find_element(By.NAME, 'price').send_keys("29.99")
        self.driver.find_element(By.XPATH, '//button[text()="Add Item"]').click()
        
        # Verify the item appears on the page
        self.assertIn(item_name, self.driver.page_source)
        
        # Verify the item was added to the file
        with open('items.txt', 'r') as f:
            items = [json.loads(line) for line in f.readlines()]
            self.assertTrue(any(item['name'] == item_name for item in items))

if __name__ == '__main__':
    unittest.main()
