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
        self.driver.get('http://localhost:8064')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "pass123")
        # Verify that the Product Listing Page has loaded
        self.assertIn("Product Listing", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.ID, 'username').send_keys(new_username)
        self.driver.find_element(By.ID, 'password').send_keys(new_password)
        self.driver.find_element(By.ID, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_browse_product_list(self):
        # Functionalities 3: Test browsing product list
        self.login("admin", "pass123")
        # Verify that the Product Listing Page shows products
        products = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(products), 0, "No products found.")

    def test_add_product_to_cart(self):
        # Functionalities 4: Test adding product to shopping cart
        self.login("admin", "pass123")
        # Add the first product to the cart
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()
        time.sleep(1)  # Wait for the action to complete

        # Verify that the product is added to the cart
        self.driver.find_element(By.LINK_TEXT, 'Shopping Cart').click()
        time.sleep(1)  # Wait for the next page to load
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "No items in the cart.")

    def test_view_shopping_cart(self):
        # Functionalities 5: Test viewing shopping cart
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Shopping Cart').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Shopping Cart Page displays items
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "Shopping cart is empty.")

    def test_remove_items_from_cart(self):
        # Functionalities 6: Test removing items from shopping cart
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()
        time.sleep(1)  # Wait for the action to complete
        self.driver.find_element(By.LINK_TEXT, 'Shopping Cart').click()
        time.sleep(1)  # Wait for the next page to load

        # Remove the first item from the cart
        self.driver.find_element(By.LINK_TEXT, 'Remove').click()
        time.sleep(1)  # Wait for the action to complete

        # Verify that the cart is empty
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(cart_items), 0, "Items still present in the cart.")

    def test_checkout_process(self):
        # Functionalities 7: Test checkout process
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()
        time.sleep(1)  # Wait for the action to complete
        self.driver.find_element(By.LINK_TEXT, 'Shopping Cart').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out checkout form
        self.driver.find_element(By.ID, 'shipping_address').send_keys("123 Main St")
        self.driver.find_element(By.ID, 'payment_info').send_keys("Visa 1234")
        self.driver.find_element(By.XPATH, '//button[text()="Place Order"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Order Confirmation Page has loaded
        self.assertIn("Order Confirmation", self.driver.title)

    def test_confirm_order(self):
        # Functionalities 8: Test confirming order
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()
        time.sleep(1)  # Wait for the action to complete
        self.driver.find_element(By.LINK_TEXT, 'Shopping Cart').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out checkout form
        self.driver.find_element(By.ID, 'shipping_address').send_keys("123 Main St")
        self.driver.find_element(By.ID, 'payment_info').send_keys("Visa 1234")
        self.driver.find_element(By.XPATH, '//button[text()="Place Order"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Order Confirmation Page has loaded
        self.assertIn("Order Confirmation", self.driver.title)

    def test_view_order_confirmation(self):
        # Functionalities 9: Test viewing order confirmation
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()
        time.sleep(1)  # Wait for the action to complete
        self.driver.find_element(By.LINK_TEXT, 'Shopping Cart').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out checkout form
        self.driver.find_element(By.ID, 'shipping_address').send_keys("123 Main St")
        self.driver.find_element(By.ID, 'payment_info').send_keys("Visa 1234")
        self.driver.find_element(By.XPATH, '//button[text()="Place Order"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Order Confirmation Page displays the order summary
        self.assertIn("Order Confirmation", self.driver.title)

    def test_navigate_back_to_product_listing(self):
        # Functionalities 10: Test navigating back to product listing
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()
        time.sleep(1)  # Wait for the action to complete
        self.driver.find_element(By.LINK_TEXT, 'Shopping Cart').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out checkout form
        self.driver.find_element(By.ID, 'shipping_address').send_keys("123 Main St")
        self.driver.find_element(By.ID, 'payment_info').send_keys("Visa 1234")
        self.driver.find_element(By.XPATH, '//button[text()="Place Order"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Navigate back to Product Listing Page
        self.driver.find_element(By.LINK_TEXT, 'Go to Login').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Product Listing Page has loaded
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
