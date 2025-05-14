import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess
import os

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
        self.driver.get('http://localhost:8114/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.url_contains('home'))

    # Functionalities 1: User Login
    def test_user_login(self):
        """Test successful login with valid credentials"""
        self.login("admin", "admin123")
        self.assertIn("Welcome", self.driver.page_source)
        self.assertIn("http://localhost:8114/", self.driver.current_url)

    # Functionalities 2: User Registration
    def test_user_registration(self):
        """Test successful user registration"""
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.url_contains('register'))
        
        username = "testuser_" + str(int(time.time()))
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys("testpass")
        self.driver.find_element(By.NAME, 'email').send_keys(f"{username}@test.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        self.wait.until(EC.url_contains('login'))
        self.assertIn("Login", self.driver.title)

    # Functionalities 3: View Available Vintage Items
    def test_view_available_items(self):
        """Test viewing available items after login"""
        self.login("admin", "admin123")
        items = self.driver.find_elements(By.CSS_SELECTOR, 'div[style*="grid-template-columns"] > div')
        self.assertGreater(len(items), 0, "No items displayed on home page")

    # Functionalities 4: Search for a Specific Vintage Item by Name
    def test_search_items(self):
        """Test searching for items by name"""
        self.login("admin", "admin123")
        search_input = self.driver.find_element(By.NAME, 'search')
        search_input.send_keys("Laptop")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        items = self.driver.find_elements(By.CSS_SELECTOR, 'div[style*="grid-template-columns"] > div')
        self.assertEqual(len(items), 1, "Should find exactly one laptop item")
        self.assertIn("Laptop", self.driver.page_source)

    # Functionalities 5: View Details of a Selected Item
    def test_view_item_details(self):
        """Test viewing details of a specific item"""
        self.login("admin", "admin123")
        item_link = self.driver.find_element(By.LINK_TEXT, 'Details')
        item_link.click()
        
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        self.assertIn("Laptop", self.driver.page_source)
        self.assertIn("Price", self.driver.page_source)

    # Functionalities 6: Create a New Listing for Vintage Items
    def test_create_new_listing(self):
        """Test creating a new item listing"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Listing').click()
        self.wait.until(EC.url_contains('create_listing'))
        
        item_name = "Test Item " + str(int(time.time()))
        self.driver.find_element(By.NAME, 'title').send_keys(item_name)
        self.driver.find_element(By.NAME, 'description').send_keys("Test description")
        self.driver.find_element(By.NAME, 'price').send_keys("99.99")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        
        self.wait.until(EC.url_contains('home'))
        self.assertIn(item_name, self.driver.page_source)

    # Functionalities 7: Submit Item Listing
    def test_submit_item_listing(self):
        """Test submitting an item listing"""
        self.login("admin", "admin123")
        initial_item_count = len(self.driver.find_elements(By.CSS_SELECTOR, 'div[style*="grid-template-columns"] > div'))
        
        self.driver.find_element(By.LINK_TEXT, 'Create New Listing').click()
        self.wait.until(EC.url_contains('create_listing'))
        
        item_name = "Test Item " + str(int(time.time()))
        self.driver.find_element(By.NAME, 'title').send_keys(item_name)
        self.driver.find_element(By.NAME, 'description').send_keys("Test description")
        self.driver.find_element(By.NAME, 'price').send_keys("99.99")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        
        self.wait.until(EC.url_contains('home'))
        new_item_count = len(self.driver.find_elements(By.CSS_SELECTOR, 'div[style*="grid-template-columns"] > div'))
        self.assertEqual(new_item_count, initial_item_count + 1, "Item count should increase by 1")

    # Functionalities 8: View Detailed Information About a Vintage Item
    def test_view_detailed_information(self):
        """Test viewing detailed information about an item"""
        self.login("admin", "admin123")
        item_link = self.driver.find_element(By.LINK_TEXT, 'Details')
        item_title = item_link.find_element(By.XPATH, './ancestor::div/h3').text
        item_link.click()
        
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        detailed_title = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.assertEqual(item_title, detailed_title, "Item title should match between list and detail view")
        self.assertIn("Description", self.driver.page_source)
        self.assertIn("Price", self.driver.page_source)
        self.assertIn("Seller", self.driver.page_source)

    # Functionalities 9: Navigate Back to Home Page from Item Details Page
    def test_navigate_back_from_details(self):
        """Test navigating back from item details to home page"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Details').click()
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        self.wait.until(EC.url_contains('home'))
        self.assertIn("Welcome", self.driver.page_source)

    # Functionalities 10: Data Storage in Local Text Files
    def test_data_storage_in_files(self):
        """Test that new items are stored in the items.txt file"""
        initial_file_size = os.path.getsize('items.txt')
        
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Listing').click()
        self.wait.until(EC.url_contains('create_listing'))
        
        item_name = "Test Item " + str(int(time.time()))
        self.driver.find_element(By.NAME, 'title').send_keys(item_name)
        self.driver.find_element(By.NAME, 'description').send_keys("Test description")
        self.driver.find_element(By.NAME, 'price').send_keys("99.99")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        self.wait.until(EC.url_contains('home'))
        
        new_file_size = os.path.getsize('items.txt')
        self.assertGreater(new_file_size, initial_file_size, "Items file should grow after adding new item")
        
        with open('items.txt', 'r') as f:
            content = f.read()
            self.assertIn(item_name, content, "New item should appear in items.txt")

if __name__ == '__main__':
    unittest.main()
