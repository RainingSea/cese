import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineShoppingCenter(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8148')

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
        self.login("admin", "admin123")
        self.assertIn("Product Listing", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "unique_user"
        new_password = "unique_password"
        new_email = "unique_user@example.com"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the login page to load

        self.assertIn("Login", self.driver.title)

    def test_browse_product_list(self):
        # Functionalities 3: Test browsing product list
        self.login("admin", "admin123")
        self.assertIn("Product Listing", self.driver.title)

        # Check if products are displayed
        products = self.driver.find_elements(By.XPATH, '//table/tbody/tr')
        self.assertGreater(len(products), 0, "No products found.")

    def test_add_product_to_cart(self):
        # Functionalities 4: Test adding product to shopping cart
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        time.sleep(1)  # Wait for the action to complete

        # No confirmation message implemented, so we check cart contents later

    def test_view_shopping_cart(self):
        # Functionalities 5: Test viewing shopping cart
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the shopping cart page to load

        # Check if cart items are displayed
        cart_items = self.driver.find_elements(By.XPATH, '//table/tbody/tr')
        self.assertGreater(len(cart_items), 0, "Shopping cart is empty.")

    def test_remove_items_from_cart(self):
        # Functionalities 6: Test removing items from shopping cart
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the shopping cart page to load

        # Remove an item from the cart
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        time.sleep(1)  # Wait for the action to complete

        # Check if the cart is updated
        cart_items = self.driver.find_elements(By.XPATH, '//table/tbody/tr')
        self.assertEqual(len(cart_items), 0, "Item not removed from cart.")

    def test_checkout_process(self):
        # Functionalities 7: Test checkout process
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the shopping cart page to load
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)  # Wait for the checkout page to load

        self.assertIn("Checkout", self.driver.title)

    def test_confirm_order(self):
        # Functionalities 8: Test confirming order
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the shopping cart page to load
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)  # Wait for the checkout page to load

        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Main St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)  # Wait for the order confirmation page to load

        self.assertIn("Order Confirmation", self.driver.title)

    def test_view_order_confirmation(self):
        # Functionalities 9: Test viewing order confirmation
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the shopping cart page to load
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)  # Wait for the checkout page to load

        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Main St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)  # Wait for the order confirmation page to load

        # Check if order summary is displayed
        order_summary = self.driver.find_element(By.XPATH, '//h2[text()="Order Summary"]')
        self.assertIsNotNone(order_summary, "Order summary not displayed.")

    def test_navigate_back_to_product_listing(self):
        # Functionalities 10: Test navigating back to product listing
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the shopping cart page to load
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)  # Wait for the checkout page to load

        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Main St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)  # Wait for the order confirmation page to load

        self.driver.find_element(By.LINK_TEXT, 'Continue Shopping').click()
        time.sleep(1)  # Wait for the product listing page to load

        self.assertIn("Product Listing", self.driver.title)

if __name__ == '__main__':
    unittest.main()
