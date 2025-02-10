import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOnlineShoppingCenter(unittest.TestCase):

    def setUp(self):
        # Start the application server
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8670/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and stop the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Product Listing", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.NAME, 'email').send_keys("new_user@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.assertIn("Login", self.driver.title)

    def test_browse_product_list(self):
        # Functionalities 3: Browse Product List
        self.login("admin", "admin123")
        self.assertIn("Product Listing", self.driver.title)
        products = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(products), 0, "No products found.")

    def test_add_product_to_shopping_cart(self):
        # Functionalities 4: Add Product to Shopping Cart
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        cart_items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cart_items), 0, "No items in the cart.")

    def test_view_shopping_cart(self):
        # Functionalities 5: View Shopping Cart
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        self.assertIn("Your Shopping Cart", self.driver.title)

    def test_remove_items_from_shopping_cart(self):
        # Functionalities 6: Remove Items from Shopping Cart
        self.fail("Not implemented")

    def test_checkout_process(self):
        # Functionalities 7: Checkout Process
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        self.driver.find_element(By.LINK_TEXT, 'Checkout').click()
        self.assertIn("Checkout", self.driver.title)

    def test_confirm_order(self):
        # Functionalities 8: Confirm Order
        self.fail("Not implemented")

    def test_view_order_confirmation(self):
        # Functionalities 9: View Order Confirmation
        self.fail("Not implemented")

    def test_navigate_back_to_product_listing_page(self):
        # Functionalities 10: Navigate Back to Product Listing Page
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
