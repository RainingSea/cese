import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestOnlineShoppingCenter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8018/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.url_contains('/products'))

    # Functionalities 1: User Login
    def test_user_login(self):
        """Test valid user login"""
        self.login("user1", "password1")
        self.assertIn("Products", self.driver.title)
        self.assertIn("Welcome, user1!", self.driver.page_source)

    # Functionalities 2: User Registration
    def test_user_registration(self):
        """Test new user registration"""
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.title_contains("Register"))
        
        # Generate unique username
        username = f"testuser{int(time.time())}"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys("testpass123")
        self.driver.find_element(By.NAME, 'email').send_keys(f"{username}@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        self.wait.until(EC.title_contains("Login"))
        self.assertIn("Login", self.driver.title)

    # Functionalities 3: Browse Product List
    def test_browse_products(self):
        """Test product listing display"""
        self.login("user1", "password1")
        products = self.driver.find_elements(By.CSS_SELECTOR, 'table tr')[1:]  # Skip header row
        self.assertGreater(len(products), 0, "No products displayed")
        
        # Verify product details
        product_names = [p.text for p in self.driver.find_elements(By.CSS_SELECTOR, 'table tr td:nth-child(1)')]
        self.assertIn("Product A", product_names)

    # Functionalities 4: Add Product to Shopping Cart
    def test_add_to_cart(self):
        """Test adding product to cart"""
        self.login("user1", "password1")
        
        # Add first product to cart
        add_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Add to Cart"]')
        add_buttons[0].click()
        
        # Verify cart is updated (indirectly by checking cart page)
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        self.wait.until(EC.title_contains("Shopping Cart"))
        cart_items = self.driver.find_elements(By.CSS_SELECTOR, 'table tr')[1:]  # Skip header row
        self.assertGreater(len(cart_items), 0, "No items in cart")

    # Functionalities 5: View Shopping Cart
    def test_view_cart(self):
        """Test viewing cart contents"""
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        self.wait.until(EC.title_contains("Shopping Cart"))
        
        # Check if cart displays items (user1 has items in carts.txt)
        cart_items = self.driver.find_elements(By.CSS_SELECTOR, 'table tr')[1:]  # Skip header row
        self.assertGreater(len(cart_items), 0, "Cart should contain items")

    # Functionalities 6: Remove Items from Shopping Cart
    def test_remove_from_cart(self):
        """Test removing item from cart"""
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        self.wait.until(EC.title_contains("Shopping Cart"))
        
        initial_items = len(self.driver.find_elements(By.CSS_SELECTOR, 'table tr')[1:])
        remove_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Remove"]')
        if remove_buttons:
            remove_buttons[0].click()
            self.wait.until(EC.title_contains("Shopping Cart"))
            updated_items = len(self.driver.find_elements(By.CSS_SELECTOR, 'table tr')[1:])
            self.assertLess(updated_items, initial_items, "Item count should decrease after removal")

    # Functionalities 7: Checkout Process
    def test_checkout_process(self):
        """Test checkout process"""
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'View Cart').click()
        self.wait.until(EC.title_contains("Shopping Cart"))
        
        # Proceed to checkout
        self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout').click()
        self.wait.until(EC.title_contains("Checkout"))
        
        # Fill checkout form
        self.driver.find_element(By.NAME, 'address').send_keys("123 Test Street")
        self.driver.find_element(By.NAME, 'payment').send_keys("Credit Card")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        
        # Verify order confirmation
        self.wait.until(EC.title_contains("Order Confirmation"))
        self.assertIn("Thank you for your order!", self.driver.page_source)

    # Functionalities 8: Confirm Order
    def test_confirm_order(self):
        """Test order confirmation"""
        self.test_checkout_process()  # Reuses checkout test
        order_id = self.driver.find_element(By.XPATH, '//p[contains(text(), "Order ID:")]').text
        self.assertTrue(order_id.startswith("Order ID:"), "Order ID should be displayed")

    # Functionalities 9: View Order Confirmation
    def test_view_order_confirmation(self):
        """Test order confirmation page"""
        self.test_checkout_process()  # Reuses checkout test
        order_details = [
            "Order ID",
            "Status",
            "Shipping Address",
            "Payment Method"
        ]
        for detail in order_details:
            self.assertIn(detail, self.driver.page_source, f"{detail} should be displayed")

    # Functionalities 10: Navigate Back to Product Listing Page
    def test_navigate_back_to_products(self):
        """Test navigation back to products from confirmation"""
        self.test_checkout_process()  # Reuses checkout test
        self.driver.find_element(By.LINK_TEXT, 'Continue Shopping').click()
        self.wait.until(EC.title_contains("Products"))
        self.assertIn("Products", self.driver.title)

if __name__ == '__main__':
    unittest.main()
