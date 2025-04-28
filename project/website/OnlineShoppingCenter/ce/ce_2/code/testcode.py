import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOnlineShoppingCenter(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8372/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
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
        # Functionalities 3: Test browsing product list
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()  # Navigate to product listing
        self.assertIn("Products", self.driver.title)  # Check if product listing page is displayed

    def test_add_product_to_cart(self):
        # Functionalities 4: Test adding product to shopping cart
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()  # Click the first product's add to cart
        self.assertIn("Your Shopping Cart", self.driver.page_source)  # Check if redirected to shopping cart

    def test_view_shopping_cart(self):
        # Functionalities 5: Test viewing shopping cart
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        self.assertIn("Your Shopping Cart", self.driver.title)  # Check if shopping cart page is displayed

    def test_remove_item_from_cart(self):
        # Functionalities 6: Test removing item from shopping cart
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()  # Add product to cart
        self.driver.find_element(By.LINK_TEXT, 'Remove').click()  # Remove the product
        self.assertNotIn("Product 1", self.driver.page_source)  # Check if product is removed

    def test_checkout_process(self):
        # Functionalities 7: Test checkout process
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()  # Add product to cart
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()  # Go to checkout
        self.assertIn("Checkout", self.driver.title)  # Check if checkout page is displayed

    def test_confirm_order(self):
        # Functionalities 8: Test confirming order
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()  # Add product to cart
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()  # Go to checkout
        self.driver.find_element(By.NAME, 'address').send_keys("123 Main St")
        self.driver.find_element(By.NAME, 'payment').send_keys("4111111111111111")  # Dummy card number
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        self.assertIn("Order Confirmation", self.driver.title)  # Check if order confirmation page is displayed

    def test_view_order_confirmation(self):
        # Functionalities 9: Test viewing order confirmation
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()  # Add product to cart
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()  # Go to checkout
        self.driver.find_element(By.NAME, 'address').send_keys("123 Main St")
        self.driver.find_element(By.NAME, 'payment').send_keys("4111111111111111")  # Dummy card number
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        self.assertIn("Your order has been confirmed!", self.driver.page_source)  # Check order confirmation message

    def test_navigate_back_to_product_listing(self):
        # Functionalities 10: Test navigating back to product listing
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()  # Add product to cart
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()  # Go to checkout
        self.driver.find_element(By.LINK_TEXT, 'Return to Products').click()  # Navigate back
        self.assertIn("Products", self.driver.title)  # Check if product listing page is displayed

if __name__ == '__main__':
    unittest.main()
