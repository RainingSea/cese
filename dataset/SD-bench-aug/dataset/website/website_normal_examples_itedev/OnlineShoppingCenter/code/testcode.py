import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineShoppingCenter(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/login')

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
        self.assertIn("Product Listing", self.driver.title)

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

        # Verify the user is redirected to the login page with a success message
        self.assertIn("Login", self.driver.title)
        self.assertIn("Registration successful! Please log in.", self.driver.page_source)

    def test_browse_product_list(self):
        # Functionalities 3: Test browsing product list
        self.login("admin", "pass123")
        # Verify that the Product Listing Page displays products
        products = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(products), 0, "No products found.")

    def test_add_product_to_cart(self):
        # Functionalities 4: Test adding product to shopping cart
        self.login("admin", "pass123")
        # Add the first product to the cart
        self.driver.find_element(By.XPATH, '(//button[text()="Add to Cart"])[1]').click()
        time.sleep(1)  # Wait for the action to complete
        # Verify that a confirmation message is displayed
        self.assertIn("Added", self.driver.page_source)

    def test_view_shopping_cart(self):
        # Functionalities 5: Test viewing shopping cart
        self.login("admin", "pass123")
        # Navigate to the Shopping Cart Page
        self.driver.get('http://localhost:5000/shopping_cart')
        # Verify that the Shopping Cart Page displays items
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "No items in the shopping cart.")

    def test_remove_items_from_cart(self):
        # Functionalities 6: Test removing items from shopping cart
        self.login("admin", "pass123")
        # Navigate to the Shopping Cart Page
        self.driver.get('http://localhost:5000/shopping_cart')
        # Remove the first item from the cart
        self.driver.find_element(By.XPATH, '(//button[text()="Remove"])[1]').click()
        time.sleep(1)  # Wait for the action to complete
        # Verify that the item is removed
        self.assertNotIn("Product A", self.driver.page_source)

    def test_checkout_process(self):
        # Functionalities 7: Test checkout process
        self.login("admin", "pass123")
        # Navigate to the Shopping Cart Page
        self.driver.get('http://localhost:5000/shopping_cart')
        # Proceed to Checkout
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()
        time.sleep(1)  # Wait for the next page to load
        # Verify that the Checkout Page has loaded
        self.assertIn("Checkout", self.driver.title)

    def test_confirm_order(self):
        # Functionalities 8: Test confirming order
        self.login("admin", "pass123")
        # Navigate to the Checkout Page
        self.driver.get('http://localhost:5000/checkout')
        # Fill out the checkout form
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Main St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Place Order"]').click()
        time.sleep(1)  # Wait for the next page to load
        # Verify that the Order Confirmation Page has loaded
        self.assertIn("Order Confirmation", self.driver.title)

    def test_view_order_confirmation(self):
        # Functionalities 9: Test viewing order confirmation
        self.login("admin", "pass123")
        # Navigate to the Order Confirmation Page
        self.driver.get('http://localhost:5000/order_confirmation')
        # Verify that the Order Confirmation Page displays order details
        self.assertIn("Your order has been placed successfully!", self.driver.page_source)

    def test_navigate_back_to_product_listing(self):
        # Functionalities 10: Test navigating back to product listing page
        self.login("admin", "pass123")
        # Navigate to the Order Confirmation Page
        self.driver.get('http://localhost:5000/order_confirmation')
        # Click the "Continue Shopping" button
        self.driver.find_element(By.LINK_TEXT, 'Continue Shopping').click()
        time.sleep(1)  # Wait for the next page to load
        # Verify that the Product Listing Page has loaded
        self.assertIn("Product Listing", self.driver.title)

if __name__ == '__main__':
    unittest.main()
