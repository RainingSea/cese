import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOnlineShoppingCenter(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8207/')  # Access the login page

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
        self.login("user1", "user123")
        self.assertIn("Products", self.driver.title)  # Check if redirected to product listing

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        
        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_browse_product_list(self):
        # Functionalities 3: Test browsing product list after login
        self.login("user1", "user123")
        self.driver.get('http://localhost:8207/product_listing')
        
        # Verify that the product listing page displays products
        products = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(products), 0, "No products found.")

    def test_add_product_to_cart(self):
        # Functionalities 4: Test adding product to shopping cart
        self.login("user1", "user123")
        self.driver.get('http://localhost:8207/product_listing')
        self.driver.find_element(By.XPATH, '//a[text()="Add to Cart"]').click()

        # Verify that the product is added to the cart
        self.driver.get('http://localhost:8207/shopping_cart')
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "Cart is empty.")

    def test_view_shopping_cart(self):
        # Functionalities 5: Test viewing shopping cart
        self.login("user1", "user123")
        self.driver.get('http://localhost:8207/shopping_cart')

        # Verify that the shopping cart page displays items
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "Shopping cart is empty.")

    def test_remove_item_from_cart(self):
        # Functionalities 6: Test removing item from shopping cart
        self.login("user1", "user123")
        self.driver.get('http://localhost:8207/product_listing')
        self.driver.find_element(By.XPATH, '//a[text()="Add to Cart"]').click()
        self.driver.get('http://localhost:8207/shopping_cart')
        self.driver.find_element(By.XPATH, '//a[text()="Remove"]').click()

        # Verify that the cart is empty after removal
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(cart_items), 0, "Cart should be empty after removal.")

    def test_checkout_process(self):
        # Functionalities 7: Test checkout process
        self.login("user1", "user123")
        self.driver.get('http://localhost:8207/product_listing')
        self.driver.find_element(By.XPATH, '//a[text()="Add to Cart"]').click()
        self.driver.get('http://localhost:8207/checkout')

        # Fill out the checkout form
        self.driver.find_element(By.NAME, 'address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()

        # Verify that the user is redirected to the order confirmation page
        self.assertIn("Order Confirmation", self.driver.title)

    def test_view_order_confirmation(self):
        # Functionalities 9: Test viewing order confirmation
        self.login("user1", "user123")
        self.driver.get('http://localhost:8207/product_listing')
        self.driver.find_element(By.XPATH, '//a[text()="Add to Cart"]').click()
        self.driver.get('http://localhost:8207/checkout')
        self.driver.find_element(By.NAME, 'address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        self.driver.get('http://localhost:8207/order_confirmation')

        # Verify that the order confirmation page displays order details
        self.assertIn("Your order has been confirmed!", self.driver.page_source)

    def test_navigate_back_to_product_listing(self):
        # Functionalities 10: Test navigation back to product listing
        self.login("user1", "user123")
        self.driver.get('http://localhost:8207/order_confirmation')
        self.driver.find_element(By.LINK_TEXT, 'Back to Products').click()

        # Verify that the user is redirected back to the product listing page
        self.assertIn("Products", self.driver.title)

if __name__ == '__main__':
    unittest.main()
