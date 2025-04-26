import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestOnlineShoppingCenter(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8208/')  # Adjusted to the correct port

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:8208/')  # Navigate to login page
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Products", self.driver.title)  # Assuming the title changes to "Products" after login

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.get('http://localhost:8208/register')  # Navigate to registration page
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.NAME, 'email').send_keys("new_user@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_browse_product_list(self):
        # Functionalities 3: Test browsing product list
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8208/product_listing')  # Navigate to product listing page

        # Verify that the product listing page displays products
        products = self.driver.find_elements(By.TAG_NAME, 'li')  # Assuming products are listed in <li> tags
        self.assertGreater(len(products), 0, "No products found.")

    def test_add_product_to_cart(self):
        # Functionalities 4: Test adding product to shopping cart
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8208/product_listing')  # Navigate to product listing page
        self.driver.find_element(By.XPATH, '//a[text()="Add to Cart"]').click()  # Click the first "Add to Cart" link

        # Verify that the product is added to the cart
        self.driver.get('http://localhost:8208/shopping_cart')  # Navigate to shopping cart page
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "Shopping cart is empty.")

    def test_view_shopping_cart(self):
        # Functionalities 5: Test viewing shopping cart
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8208/shopping_cart')  # Navigate to shopping cart page

        # Verify that the shopping cart page displays items
        items = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(items), 0, "Shopping cart is empty.")

    def test_checkout_process(self):
        # Functionalities 7: Test checkout process
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8208/shopping_cart')  # Navigate to shopping cart page
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()  # Click checkout button

        # Fill out the checkout form
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Main St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")  # Example card number
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()

        # Verify that the order confirmation page is displayed
        self.assertIn("Order Confirmation", self.driver.title)

    def test_view_order_confirmation(self):
        # Functionalities 9: Test viewing order confirmation
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8208/shopping_cart')  # Navigate to shopping cart page
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()  # Click checkout button
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Main St")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("4111111111111111")  # Example card number
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()

        # Verify that the order confirmation page displays the order summary
        self.assertIn("Your order has been confirmed!", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
