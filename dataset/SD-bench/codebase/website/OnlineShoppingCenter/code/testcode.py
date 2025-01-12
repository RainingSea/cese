import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineShoppingCenter(unittest.TestCase):

    def setUp(self):
        # Start the web server
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start

        # Initialize the webdriver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8315/login')

    def tearDown(self):
        # Close the web driver session and stop the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Products", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 2: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        self.assertIn("Login", self.driver.title)

    def test_browse_product_list(self):
        # Functionalities 3: Browse Product List
        self.login("admin", "admin123")
        self.assertIn("Product 1", self.driver.page_source)
        self.assertIn("Product 2", self.driver.page_source)
        self.assertIn("Product 3", self.driver.page_source)

    def test_add_product_to_shopping_cart(self):
        # Functionalities 4: Add Product to Shopping Cart
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()
        time.sleep(1)
        self.assertIn("Product 1", self.driver.page_source)

    def test_view_shopping_cart(self):
        # Functionalities 5: View Shopping Cart
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.assertIn("Shopping Cart", self.driver.title)

    def test_remove_items_from_shopping_cart(self):
        # Functionalities 6: Remove Items from Shopping Cart
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Remove').click()
        time.sleep(1)
        self.assertNotIn("Product 1", self.driver.page_source)

    def test_checkout_process(self):
        # Functionalities 7: Checkout Process
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)
        self.assertIn("Checkout", self.driver.title)

    def test_confirm_order(self):
        # Functionalities 8: Confirm Order
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Main St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)
        self.assertIn("Order Confirmation", self.driver.title)

    def test_view_order_confirmation(self):
        # Functionalities 9: View Order Confirmation
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Main St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)
        self.assertIn("Your order has been confirmed!", self.driver.page_source)

    def test_navigate_back_to_product_listing_page(self):
        # Functionalities 10: Navigate Back to Product Listing Page
        self.fail("not implemented")

if __name__ == '__main__':
    unittest.main()
