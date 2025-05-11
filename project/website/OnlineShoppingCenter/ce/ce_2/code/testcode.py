import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOnlineShoppingCenter(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8486/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        
        # Verify that the user is redirected to the Product Listing Page
        self.assertIn("Products", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        
        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.NAME, 'email').send_keys("new_user@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_browse_product_list(self):
        # Functionalities 3: Test browsing product list
        self.login("admin", "admin123")
        
        # Verify that the Product Listing Page displays products
        products = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(products), 0, "No products found.")

    def test_add_product_to_cart(self):
        # Functionalities 4: Test adding product to shopping cart
        self.login("admin", "admin123")
        
        # Click the "Add to Cart" button for the first product
        self.driver.find_element(By.XPATH, '//a[text()="Add to Cart"]').click()

        # Verify that the product is added to the cart
        self.driver.get('http://localhost:8486/shopping_cart')
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "Cart is empty.")

    def test_view_shopping_cart(self):
        # Functionalities 5: Test viewing shopping cart
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8486/shopping_cart')

        # Verify that the Shopping Cart Page displays items
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "Shopping cart is empty.")

    def test_remove_items_from_cart(self):
        # Functionalities 6: Test removing items from shopping cart
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//a[text()="Add to Cart"]').click()
        self.driver.get('http://localhost:8486/shopping_cart')

        # Click the "Remove" button for the first item
        self.driver.find_element(By.XPATH, '//a[text()="Remove"]').click()

        # Verify that the cart is empty
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(cart_items), 0, "Cart should be empty after removal.")

    def test_checkout_process(self):
        # Functionalities 7: Test checkout process
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//a[text()="Add to Cart"]').click()
        self.driver.get('http://localhost:8486/checkout')

        # Fill out the shipping address and payment information
        self.driver.find_element(By.NAME, 'address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment_method').send_keys("Credit Card")
        self.driver.find_element(By.XPATH, '//button[text()="Place Order"]').click()

        # Verify that the user is redirected to the Order Confirmation Page
        self.assertIn("Order Confirmed!", self.driver.page_source)

    def test_confirm_order(self):
        # Functionalities 8: Test confirming order
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//a[text()="Add to Cart"]').click()
        self.driver.get('http://localhost:8486/checkout')
        self.driver.find_element(By.NAME, 'address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment_method').send_keys("Credit Card")
        self.driver.find_element(By.XPATH, '//button[text()="Place Order"]').click()

        # Verify that the order confirmation page displays the order summary
        self.assertIn("Order Confirmed!", self.driver.page_source)

    def test_navigate_back_to_product_listing(self):
        # Functionalities 10: Test navigation back to product listing
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//a[text()="Add to Cart"]').click()
        self.driver.get('http://localhost:8486/checkout')
        self.driver.find_element(By.LINK_TEXT, 'Continue Shopping').click()

        # Verify that the user is redirected back to the Product Listing Page
        self.assertIn("Products", self.driver.title)

if __name__ == '__main__':
    unittest.main()
