import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineShoppingCenter(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the web application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

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
        self.login("testuser", "testpass")

        # Verify that the user is redirected to the Product Listing Page
        self.assertIn("Product Listing", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the registration page to load

        # Input registration details
        self.driver.find_element(By.NAME, 'username').send_keys("newuser")
        self.driver.find_element(By.NAME, 'password').send_keys("newpass")
        self.driver.find_element(By.NAME, 'email').send_keys("newuser@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the login page to load

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_browse_product_list(self):
        # Functionalities 3: Test browsing product list
        self.login("testuser", "testpass")

        # Verify that the product listing page displays products
        products = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(products), 0, "No products found.")

    def test_add_product_to_shopping_cart(self):
        # Functionalities 4: Test adding product to shopping cart
        self.login("testuser", "testpass")

        # Add the first product to the cart
        self.driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        time.sleep(1)  # Wait for the action to complete

        # Verify that the product is added to the cart
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "No items in the cart.")

    def test_view_shopping_cart(self):
        # Functionalities 5: Test viewing shopping cart
        self.login("testuser", "testpass")

        # Navigate to the shopping cart page
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)

        # Verify that the cart displays items
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "No items in the cart.")

    def test_remove_items_from_shopping_cart(self):
        # Functionalities 6: Test removing items from shopping cart
        self.login("testuser", "testpass")

        # Add a product to the cart and then remove it
        self.driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        time.sleep(1)

        # Verify that the cart is empty
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(cart_items), 0, "Cart is not empty.")

    def test_checkout_process(self):
        # Functionalities 7: Test checkout process
        self.login("testuser", "testpass")

        # Add a product to the cart and proceed to checkout
        self.driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)

        # Verify that the checkout page is displayed
        self.assertIn("Checkout", self.driver.title)

    def test_confirm_order(self):
        # Functionalities 8: Test order confirmation
        self.login("testuser", "testpass")

        # Add a product to the cart, proceed to checkout, and confirm order
        self.driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)

        # Verify that the order confirmation page is displayed
        self.assertIn("Order Confirmation", self.driver.title)

    def test_view_order_confirmation(self):
        # Functionalities 9: Test viewing order confirmation
        self.login("testuser", "testpass")

        # Add a product to the cart, proceed to checkout, and confirm order
        self.driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)

        # Verify that the order confirmation page displays order details
        self.assertIn("Your order has been confirmed!", self.driver.page_source)

    def test_navigate_back_to_product_listing_page(self):
        # Functionalities 10: Test navigation back to product listing page
        self.login("testuser", "testpass")

        # Add a product to the cart, proceed to checkout, and confirm order
        self.driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)

        # Click "Continue Shopping" and verify redirection to product listing
        self.driver.find_element(By.LINK_TEXT, 'Continue Shopping').click()
        time.sleep(1)
        self.assertIn("Product Listing", self.driver.title)

if __name__ == '__main__':
    unittest.main()
