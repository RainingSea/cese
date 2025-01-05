import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineShoppingCenter(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8058/')  # Access the login page

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin1", "pass123")

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
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the login page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.page_source)

    def test_browse_product_list(self):
        # Functionalities 3: Test browsing product list
        self.login("admin1", "pass123")

        # Verify that the Product Listing Page displays products
        products = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(products), 0, "No products found.")

    def test_add_product_to_cart(self):
        # Functionalities 4: Test adding product to shopping cart
        self.login("admin1", "pass123")

        # Add the first product to the cart
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()
        time.sleep(1)  # Wait for the page to update

        # Verify that the product is added to the cart
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "No items in the cart.")

    def test_view_shopping_cart(self):
        # Functionalities 5: Test viewing shopping cart
        self.login("admin1", "pass123")

        # Navigate to the Shopping Cart Page
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)

        # Verify that the cart displays products
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "No items in the cart.")

    def test_remove_items_from_cart(self):
        # Functionalities 6: Test removing items from shopping cart
        self.fail("Not implemented")

    def test_checkout_process(self):
        # Functionalities 7: Test checkout process
        self.login("admin1", "pass123")

        # Navigate to the Shopping Cart Page and proceed to checkout
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//input[@value="Checkout"]').click()
        time.sleep(1)

        # Verify that the Checkout Page is displayed
        self.assertIn("Checkout", self.driver.page_source)

    def test_confirm_order(self):
        # Functionalities 8: Test order confirmation
        self.fail("Not implemented")

    def test_view_order_confirmation(self):
        # Functionalities 9: Test viewing order confirmation
        self.fail("Not implemented")

    def test_navigate_back_to_product_listing(self):
        # Functionalities 10: Test navigating back to product listing
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
