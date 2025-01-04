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
        self.driver.get('http://localhost:8147')

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
        self.login("admin", "adminpass")
        # Verify redirection to Product Listing Page
        self.assertIn("Products", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input registration details
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for redirection

        # Verify redirection to Login Page
        self.assertIn("Login", self.driver.page_source)

    def test_browse_product_list(self):
        # Functionalities 3: Test browsing product list
        self.login("admin", "adminpass")
        # Verify product list is displayed
        self.assertIn("Product A", self.driver.page_source)
        self.assertIn("Product B", self.driver.page_source)
        self.assertIn("Product C", self.driver.page_source)

    def test_add_product_to_cart(self):
        # Functionalities 4: Test adding product to shopping cart
        self.login("admin", "adminpass")
        self.driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        time.sleep(1)  # Wait for the cart update

        # Verify product is added to cart
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for cart page to load
        self.assertIn("Product A", self.driver.page_source)

    def test_view_shopping_cart(self):
        # Functionalities 5: Test viewing shopping cart
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for cart page to load

        # Verify cart contents
        self.assertIn("Your Shopping Cart", self.driver.page_source)

    def test_remove_items_from_cart(self):
        # Functionalities 6: Test removing items from shopping cart
        self.login("admin", "adminpass")
        self.driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        time.sleep(1)  # Wait for the cart update

        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for cart page to load
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        time.sleep(1)  # Wait for the cart update

        # Verify product is removed from cart
        self.assertNotIn("Product A", self.driver.page_source)

    def test_checkout_process(self):
        # Functionalities 7: Test checkout process
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for cart page to load
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)  # Wait for checkout page to load

        # Verify checkout page
        self.assertIn("Checkout", self.driver.page_source)

    def test_confirm_order(self):
        # Functionalities 8: Test order confirmation
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for cart page to load
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)  # Wait for checkout page to load

        # Fill out checkout form
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Place Order"]').click()
        time.sleep(1)  # Wait for order confirmation

        # Verify order confirmation
        self.assertIn("Order Confirmation", self.driver.page_source)

    def test_view_order_confirmation(self):
        # Functionalities 9: Test viewing order confirmation
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for cart page to load
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)  # Wait for checkout page to load

        # Fill out checkout form
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Place Order"]').click()
        time.sleep(1)  # Wait for order confirmation

        # Verify order summary
        self.assertIn("Order Summary", self.driver.page_source)

    def test_navigate_back_to_product_listing(self):
        # Functionalities 10: Test navigation back to product listing
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for cart page to load
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)  # Wait for checkout page to load

        # Fill out checkout form
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Place Order"]').click()
        time.sleep(1)  # Wait for order confirmation

        # Navigate back to product listing
        self.driver.find_element(By.LINK_TEXT, 'Continue Shopping').click()
        time.sleep(1)  # Wait for product listing page to load

        # Verify redirection to Product Listing Page
        self.assertIn("Products", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
