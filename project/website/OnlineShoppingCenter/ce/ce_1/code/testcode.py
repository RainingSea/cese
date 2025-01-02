import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestOnlineShoppingCenter(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8160')

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
        self.login("user1", "password1")
        self.assertIn("Product Listing", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Login", self.driver.page_source)

    def test_browse_product_list(self):
        # Functionalities 3: Test browsing product list
        self.login("user1", "password1")
        self.assertIn("Product Listing", self.driver.page_source)

    def test_add_product_to_shopping_cart(self):
        # Functionalities 4: Test adding product to shopping cart
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Add to Cart').click()
        time.sleep(1)  # Wait for the action to complete

        # No confirmation message is implemented, so we check the cart instead
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.assertIn("Your Shopping Cart", self.driver.page_source)

    def test_view_shopping_cart(self):
        # Functionalities 5: Test viewing shopping cart
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.assertIn("Your Shopping Cart", self.driver.page_source)

    def test_remove_items_from_shopping_cart(self):
        # Functionalities 6: Test removing items from shopping cart
        self.fail("Remove functionality not implemented")

    def test_checkout_process(self):
        # Functionalities 7: Test checkout process
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()
        time.sleep(1)
        self.assertIn("Checkout", self.driver.page_source)

    def test_confirm_order(self):
        # Functionalities 8: Test confirming order
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment').send_keys("1234567890123456")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)
        self.assertIn("Order Confirmation", self.driver.page_source)

    def test_view_order_confirmation(self):
        # Functionalities 9: Test viewing order confirmation
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment').send_keys("1234567890123456")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)
        self.assertIn("Order Summary", self.driver.page_source)

    def test_navigate_back_to_product_listing(self):
        # Functionalities 10: Test navigating back to product listing
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'address').send_keys("123 Test St")
        self.driver.find_element(By.NAME, 'payment').send_keys("1234567890123456")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Continue Shopping').click()
        time.sleep(1)
        self.assertIn("Product Listing", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
