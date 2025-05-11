import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOnlineShoppingCenter(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8485/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the application
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
        self.assertIn("Products", self.driver.title)  # Check if redirected to product listing

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        
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
        # Functionalities 3: Test browsing product list
        self.login("admin", "admin123")
        
        # Verify that the product listing page displays products
        products = self.driver.find_elements(By.TAG_NAME, 'h2')
        self.assertGreater(len(products), 0, "No products found.")

    def test_add_product_to_cart(self):
        # Functionalities 4: Test adding product to shopping cart
        self.login("admin", "admin123")
        
        # Click the "Add to Cart" button for the first product
        self.driver.find_element(By.XPATH, '//a[contains(@href, "/add_to_cart/1")]').click()
        
        # Verify that the product is added to the cart
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "Cart is empty.")

    def test_view_shopping_cart(self):
        # Functionalities 5: Test viewing shopping cart
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        
        # Verify that the shopping cart page is displayed
        self.assertIn("Your Shopping Cart", self.driver.page_source)

    def test_remove_items_from_cart(self):
        # Functionalities 6: Test removing items from shopping cart
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//a[contains(@href, "/add_to_cart/1")]').click()
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        
        # Click the "Remove" button for the first item
        self.driver.find_element(By.XPATH, '//a[contains(@href, "/remove_from_cart/1")]').click()
        
        # Verify the cart is empty
        self.assertNotIn("1", self.driver.page_source)

    def test_checkout_process(self):
        # Functionalities 7: Test checkout process
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//a[contains(@href, "/add_to_cart/1")]').click()
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        
        # Fill out the shipping information
        self.driver.find_element(By.NAME, 'shipping_info').send_keys("123 Main St")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        
        # Verify that the order confirmation page is displayed
        self.assertIn("Order Confirmation", self.driver.page_source)

    def test_confirm_order(self):
        # Functionalities 8: Test confirming order
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//a[contains(@href, "/add_to_cart/1")]').click()
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        
        # Fill out the shipping information
        self.driver.find_element(By.NAME, 'shipping_info').send_keys("123 Main St")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        
        # Verify that the order confirmation page is displayed
        self.assertIn("Your order has been placed successfully!", self.driver.page_source)

    def test_view_order_confirmation(self):
        # Functionalities 9: Test viewing order confirmation
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//a[contains(@href, "/add_to_cart/1")]').click()
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        
        # Fill out the shipping information
        self.driver.find_element(By.NAME, 'shipping_info').send_keys("123 Main St")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        
        # Verify that the order confirmation page is displayed
        self.assertIn("Your order has been placed successfully!", self.driver.page_source)

    def test_navigate_back_to_product_listing(self):
        # Functionalities 10: Test navigating back to product listing page
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//a[contains(@href, "/add_to_cart/1")]').click()
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        
        # Fill out the shipping information
        self.driver.find_element(By.NAME, 'shipping_info').send_keys("123 Main St")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        
        # Click the continue shopping link
        self.driver.find_element(By.LINK_TEXT, 'Continue Shopping').click()
        
        # Verify that the product listing page is displayed
        self.assertIn("Products", self.driver.title)

if __name__ == '__main__':
    unittest.main()
