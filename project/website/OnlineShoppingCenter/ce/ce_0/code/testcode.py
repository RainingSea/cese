import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineShoppingCenter(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8206/') 

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
        self.assertIn("Products", self.driver.title)  # Assuming the title changes to "Products" after login

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_browse_product_list(self):
        # Functionalities 3: Test browsing product list
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8206/')  # Navigate to product listing page
        time.sleep(1)  # Wait for the page to load

        # Verify that the product listing page displays products
        products = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(products), 0, "No products found.")

    def test_add_product_to_cart(self):
        # Functionalities 4: Test adding product to shopping cart
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8206/')  # Navigate to product listing page
        time.sleep(1)  # Wait for the page to load

        # Click the "Add to Cart" button for the first product
        self.driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        time.sleep(1)  # Wait for the action to complete

        # Verify that the product was added to the cart
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the cart page to load
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "Cart is empty.")

    def test_view_shopping_cart(self):
        # Functionalities 5: Test viewing shopping cart
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8206/')  # Navigate to product listing page
        time.sleep(1)  # Wait for the page to load

        # Add a product to the cart
        self.driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        time.sleep(1)  # Wait for the action to complete

        # Navigate to the shopping cart
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the cart page to load

        # Verify that the cart displays the correct items
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "Cart is empty.")

    def test_remove_items_from_cart(self):
        # Functionalities 6: Test removing items from shopping cart
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8206/')  # Navigate to product listing page
        time.sleep(1)  # Wait for the page to load

        # Add a product to the cart
        self.driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        time.sleep(1)  # Wait for the action to complete

        # Navigate to the shopping cart
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the cart page to load

        # Remove the product from the cart
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        time.sleep(1)  # Wait for the action to complete

        # Verify that the cart is empty
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(cart_items), 0, "Cart is not empty.")

    def test_checkout_process(self):
        # Functionalities 7: Test checkout process
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8206/')  # Navigate to product listing page
        time.sleep(1)  # Wait for the page to load

        # Add a product to the cart
        self.driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        time.sleep(1)  # Wait for the action to complete

        # Navigate to the shopping cart
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the cart page to load

        # Proceed to checkout
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()
        time.sleep(1)  # Wait for the checkout page to load

        # Fill out the checkout form
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)  # Wait for the order confirmation

        # Verify that the order confirmation page is displayed
        self.assertIn("Order Confirmation", self.driver.title)

    def test_confirm_order(self):
        # Functionalities 8: Test confirming order
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8206/')  # Navigate to product listing page
        time.sleep(1)  # Wait for the page to load

        # Add a product to the cart and proceed to checkout
        self.driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        time.sleep(1)  # Wait for the action to complete
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the cart page to load
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()
        time.sleep(1)  # Wait for the checkout page to load

        # Fill out the checkout form
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)  # Wait for the order confirmation

        # Verify that the order confirmation page is displayed
        self.assertIn("Order Confirmation", self.driver.title)

    def test_view_order_confirmation(self):
        # Functionalities 9: Test viewing order confirmation
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8206/')  # Navigate to product listing page
        time.sleep(1)  # Wait for the page to load

        # Add a product to the cart and proceed to checkout
        self.driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        time.sleep(1)  # Wait for the action to complete
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the cart page to load
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()
        time.sleep(1)  # Wait for the checkout page to load

        # Fill out the checkout form
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)  # Wait for the order confirmation

        # Verify that the order confirmation page displays the correct message
        self.assertIn("Your order has been confirmed!", self.driver.page_source)

    def test_navigate_back_to_product_listing(self):
        # Functionalities 10: Test navigating back to product listing page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8206/')  # Navigate to product listing page
        time.sleep(1)  # Wait for the page to load

        # Add a product to the cart and proceed to checkout
        self.driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        time.sleep(1)  # Wait for the action to complete
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the cart page to load
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()
        time.sleep(1)  # Wait for the checkout page to load

        # Fill out the checkout form
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)  # Wait for the order confirmation

        # Navigate back to product listing
        self.driver.find_element(By.LINK_TEXT, 'Continue Shopping').click()
        time.sleep(1)  # Wait for the product listing page to load

        # Verify that the product listing page is displayed
        self.assertIn("Products", self.driver.title)

if __name__ == '__main__':
    unittest.main()
