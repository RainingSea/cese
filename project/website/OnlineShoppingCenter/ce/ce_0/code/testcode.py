import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestOnlineShoppingCenter(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8669/')  # Access the login page

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
        # Verify that the Product Listing Page has loaded
        self.assertIn("Products", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
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
        self.assertIn("Login", self.driver.page_source)

    def test_browse_product_list(self):
        # Functionalities 3: Test browsing product list
        self.login("admin", "admin123")
        # Verify that the Product Listing Page displays products
        products = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(products), 0, "No products found.")

    def test_add_product_to_shopping_cart(self):
        # Functionalities 4: Test adding product to shopping cart
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()
        time.sleep(1)  # Wait for the cart update

        # Verify that the product is added to the cart
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the cart page to load
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "No items in the cart.")

    def test_view_shopping_cart(self):
        # Functionalities 5: Test viewing shopping cart
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the cart page to load

        # Verify that the cart page displays items
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "No items in the cart.")

    def test_remove_items_from_shopping_cart(self):
        # Functionalities 6: Test removing items from shopping cart
        self.fail("Remove functionality not implemented")

    def test_checkout_process(self):
        # Functionalities 7: Test checkout process
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the cart page to load
        self.driver.find_element(By.XPATH, '//button[text()="Checkout"]').click()
        time.sleep(1)  # Wait for the checkout page to load

        # Verify that the Checkout Page has loaded
        self.assertIn("Checkout", self.driver.page_source)

    def test_confirm_order(self):
        # Functionalities 8: Test order confirmation
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the cart page to load
        self.driver.find_element(By.XPATH, '//button[text()="Checkout"]').click()
        time.sleep(1)  # Wait for the checkout page to load
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)  # Wait for the order confirmation page to load

        # Verify that the Order Confirmation Page has loaded
        self.assertIn("Order Confirmed!", self.driver.page_source)

    def test_view_order_confirmation(self):
        # Functionalities 9: Test viewing order confirmation
        self.fail("Order confirmation view not implemented")

    def test_navigate_back_to_product_listing_page(self):
        # Functionalities 10: Test navigation back to product listing page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)  # Wait for the cart page to load
        self.driver.find_element(By.XPATH, '//button[text()="Checkout"]').click()
        time.sleep(1)  # Wait for the checkout page to load
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)  # Wait for the order confirmation page to load
        self.driver.find_element(By.LINK_TEXT, 'Continue Shopping').click()
        time.sleep(1)  # Wait for the product listing page to load

        # Verify that the Product Listing Page has loaded
        self.assertIn("Products", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
