import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineShoppingCenter(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8064/') 

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
        # Functionalities 1: Test user login functionality
        self.login("admin", "pass123")

        # Verify that the Product Listing Page has loaded
        self.assertIn("Products", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the login page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.page_source)

    def test_browse_product_list(self):
        # Functionalities 3: Test browsing product list
        self.login("admin", "pass123")

        # Verify that the Product Listing Page displays products
        products = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(products), 0, "No products found.")

    def test_add_product_to_shopping_cart(self):
        # Functionalities 4: Test adding product to shopping cart
        self.fail("Not implemented")

    def test_view_shopping_cart(self):
        # Functionalities 5: Test viewing shopping cart
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Shopping Cart').click()
        time.sleep(1)  # Wait for the shopping cart page to load

        # Verify that the Shopping Cart Page displays correctly
        self.assertIn("Your Shopping Cart", self.driver.page_source)

    def test_remove_items_from_shopping_cart(self):
        # Functionalities 6: Test removing items from shopping cart
        self.fail("Not implemented")

    def test_checkout_process(self):
        # Functionalities 7: Test checkout process
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Shopping Cart').click()
        time.sleep(1)  # Wait for the shopping cart page to load
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)  # Wait for the checkout page to load

        # Fill out the checkout form
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Main St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("Visa")
        self.driver.find_element(By.XPATH, '//button[text()="Place Order"]').click()
        time.sleep(1)  # Wait for the order confirmation page to load

        # Verify that the user is redirected to the Order Confirmation Page
        self.assertIn("Order Confirmation", self.driver.page_source)

    def test_confirm_order(self):
        # Functionalities 8: Test confirming order
        self.fail("Not implemented")

    def test_view_order_confirmation(self):
        # Functionalities 9: Test viewing order confirmation
        self.fail("Not implemented")

    def test_navigate_back_to_product_listing_page(self):
        # Functionalities 10: Test navigation back to product listing page
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
