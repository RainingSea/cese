import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineVintageMarket(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web app to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8135')

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
        # Functionalities 1: User Login
        self.login("admin", "pass123")
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Login", self.driver.title)

    def test_view_available_vintage_items(self):
        # Functionalities 3: View Available Vintage Items
        self.login("admin", "pass123")
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "No vintage items found.")

    def test_search_for_specific_vintage_item(self):
        # Functionalities 4: Search for a Specific Vintage Item by Name
        self.login("admin", "pass123")
        self.driver.find_element(By.NAME, 'search').send_keys("Vintage Clock")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load
        self.assertIn("Vintage Clock", self.driver.page_source)

    def test_view_details_of_selected_item(self):
        # Functionalities 5: View Details of a Selected Item
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Vintage Clock').click()
        time.sleep(1)  # Wait for the item details page to load
        self.assertIn("Vintage Clock", self.driver.page_source)

    def test_create_new_listing(self):
        # Functionalities 6: Create a New Listing for Vintage Items
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Listing').click()
        time.sleep(1)  # Wait for the listing page to load

        self.driver.find_element(By.NAME, 'name').send_keys("Vintage Lamp")
        self.driver.find_element(By.NAME, 'description').send_keys("A beautiful vintage lamp.")
        self.driver.find_element(By.NAME, 'price').send_keys("75.00")
        self.driver.find_element(By.XPATH, '//button[text()="Create Listing"]').click()
        time.sleep(1)  # Wait for the home page to load

        self.assertIn("Vintage Lamp", self.driver.page_source)

    def test_submit_item_listing(self):
        # Functionalities 7: Submit Item Listing
        self.fail("Not implemented")

    def test_view_detailed_information_about_item(self):
        # Functionalities 8: View Detailed Information About a Vintage Item
        self.fail("Not implemented")

    def test_navigate_back_to_home_page(self):
        # Functionalities 9: Navigate Back to Home Page from Item Details Page
        self.fail("Not implemented")

    def test_data_storage_in_local_text_files(self):
        # Functionalities 10: Data Storage in Local Text Files
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
