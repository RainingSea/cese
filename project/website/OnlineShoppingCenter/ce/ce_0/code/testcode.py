import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOnlineShoppingCenter(unittest.TestCase):

    def setUp(self):
        # Start the web server and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the correct port

    def tearDown(self):
        # Close the web driver session and terminate the server process
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
        
        # Verify that the Product Listing Page has loaded
        self.assertIn("Products", self.driver.title)

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
        self.login("user1", "user123")
        
        # Verify that the Product Listing Page displays products
        self.assertIn("Product 1", self.driver.page_source)
        self.assertIn("Product 2", self.driver.page_source)

    def test_add_product_to_cart(self):
        # Functionalities 4: Test adding product to shopping cart
        self.login("user1", "user123")
        
        # Click the "Add to Cart" button for Product 1
        self.driver.find_element(By.XPATH, '//li[contains(text(), "Product 1")]/button').click()

        # Verify that the product was added to the cart
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        self.assertIn("Product 1", self.driver.page_source)

    def test_view_shopping_cart(self):
        # Functionalities 5: Test viewing shopping cart
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()

        # Verify that the Shopping Cart Page displays the correct items
        self.assertIn("Product 1", self.driver.page_source)

    def test_remove_item_from_cart(self):
        # Functionalities 6: Test removing items from shopping cart
        self.login("user1", "user123")
        self.driver.find_element(By.XPATH, '//li[contains(text(), "Product 1")]/button').click()
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()

        # Click the "Remove" button next to Product 1
        self.driver.find_element(By.XPATH, '//li[contains(text(), "Product 1")]/button[text()="Remove"]').click()

        # Verify that the product was removed from the cart
        self.assertNotIn("Product 1", self.driver.page_source)

    def test_checkout_process(self):
        # Functionalities 7: Test checkout process
        self.login("user1", "user123")
        self.driver.find_element(By.XPATH, '//li[contains(text(), "Product 1")]/button').click()
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()

        # Fill out the shipping address and payment information
        self.driver.find_element(By.NAME, 'shipping').send_keys("123 Main St")
        self.driver.find_element(By.NAME, 'payment').send_keys("Visa")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()

        # Verify that the order confirmation page is displayed
        self.assertIn("Order Confirmation", self.driver.title)

    def test_confirm_order(self):
        # Functionalities 8: Test confirming order
        self.login("user1", "user123")
        self.driver.find_element(By.XPATH, '//li[contains(text(), "Product 1")]/button').click()
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()
        self.driver.find_element(By.NAME, 'shipping').send_keys("123 Main St")
        self.driver.find_element(By.NAME, 'payment').send_keys("Visa")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()

        # Verify that the order confirmation page displays the order summary
        self.assertIn("Your order has been placed successfully!", self.driver.page_source)

    def test_navigate_back_to_product_listing(self):
        # Functionalities 10: Test navigating back to product listing page
        self.login("user1", "user123")
        self.driver.find_element(By.XPATH, '//li[contains(text(), "Product 1")]/button').click()
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        self.driver.find_element(By.LINK_TEXT, 'Back to Products').click()

        # Verify that the Product Listing Page is displayed again
        self.assertIn("Products", self.driver.title)

if __name__ == '__main__':
    unittest.main()
