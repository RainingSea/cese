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
        self.driver.get('http://localhost:8020/login')
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
        self.login("admin", "admin123")
        self.assertIn("Products", self.driver.title)
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, "View Cart").is_displayed())

    # Functionalities 2: User Registration
    def test_user_registration(self):
        """Test new user registration"""
        self.driver.find_element(By.LINK_TEXT, "Register").click()
        self.wait.until(EC.url_contains('/register'))
        
        username = "newuser_" + str(int(time.time()))
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys("newpassword123")
        self.driver.find_element(By.NAME, 'email').send_keys(f"{username}@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        self.wait.until(EC.url_contains('/login'))
        self.assertIn("Login", self.driver.title)

    # Functionalities 3: Browse Product List
    def test_browse_products(self):
        """Test product listing page"""
        self.login("admin", "admin123")
        products = self.driver.find_elements(By.CSS_SELECTOR, 'div[style*="border: 1px solid #ccc"]')
        self.assertGreaterEqual(len(products), 4)  # There should be at least 4 products
        product_names = [p.text for p in products]
        self.assertIn("Laptop", product_names[0])
        self.assertIn("Smartphone", product_names[1])

    # Functionalities 4: Add Product to Shopping Cart
    def test_add_to_cart(self):
        """Test adding product to cart"""
        self.login("admin", "admin123")
        add_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Add to Cart"]')
        add_buttons[0].click()  # Add first product (Laptop)
        
        self.driver.find_element(By.LINK_TEXT, "View Cart").click()
        self.wait.until(EC.url_contains('/cart'))
        
        cart_items = self.driver.find_elements(By.CSS_SELECTOR, 'table tr')[1:]  # Skip header row
        self.assertEqual(len(cart_items), 1)
        self.assertIn("Laptop", cart_items[0].text)

    # Functionalities 5: View Shopping Cart
    def test_view_cart(self):
        """Test viewing cart contents"""
        self.login("admin", "admin123")
        add_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Add to Cart"]')
        add_buttons[0].click()  # Add Laptop
        add_buttons[1].click()  # Add Smartphone
        
        self.driver.find_element(By.LINK_TEXT, "View Cart").click()
        self.wait.until(EC.url_contains('/cart'))
        
        cart_items = self.driver.find_elements(By.CSS_SELECTOR, 'table tr')[1:-1]  # Skip header and total rows
        self.assertEqual(len(cart_items), 2)
        self.assertIn("Laptop", cart_items[0].text)
        self.assertIn("Smartphone", cart_items[1].text)

    # Functionalities 6: Remove Items from Shopping Cart
    def test_remove_from_cart(self):
        """Test removing items from cart"""
        self.login("admin", "admin123")
        add_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Add to Cart"]')
        add_buttons[0].click()  # Add Laptop
        
        self.driver.find_element(By.LINK_TEXT, "View Cart").click()
        self.wait.until(EC.url_contains('/cart'))
        
        # Verify item is in cart
        cart_items = self.driver.find_elements(By.CSS_SELECTOR, 'table tr')[1:-1]
        self.assertEqual(len(cart_items), 1)
        
        # Remove item
        remove_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Remove"]')
        remove_buttons[0].click()
        
        # Verify cart is empty
        empty_message = self.driver.find_element(By.XPATH, '//p[contains(text(), "Your cart is empty")]')
        self.assertTrue(empty_message.is_displayed())

    # Functionalities 7: Checkout Process
    def test_checkout_process(self):
        """Test checkout process"""
        self.login("admin", "admin123")
        add_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Add to Cart"]')
        add_buttons[0].click()  # Add Laptop
        
        self.driver.find_element(By.LINK_TEXT, "View Cart").click()
        self.wait.until(EC.url_contains('/cart'))
        
        # Proceed to checkout
        self.driver.find_element(By.LINK_TEXT, "Proceed to Checkout").click()
        self.wait.until(EC.url_contains('/checkout'))
        
        # Fill checkout form
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Test Street")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("Visa 1234 5678 9012 3456")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        
        # Verify order confirmation
        self.wait.until(EC.url_contains('/confirm/'))
        self.assertIn("Order Confirmation", self.driver.title)

    # Functionalities 8: Confirm Order
    def test_confirm_order(self):
        """Test order confirmation"""
        self.login("admin", "admin123")
        add_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Add to Cart"]')
        add_buttons[0].click()  # Add Laptop
        
        self.driver.find_element(By.LINK_TEXT, "View Cart").click()
        self.wait.until(EC.url_contains('/cart'))
        
        self.driver.find_element(By.LINK_TEXT, "Proceed to Checkout").click()
        self.wait.until(EC.url_contains('/checkout'))
        
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Test Street")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("Visa 1234 5678 9012 3456")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        
        self.wait.until(EC.url_contains('/confirm/'))
        order_id = self.driver.find_element(By.TAG_NAME, 'h2').text
        self.assertTrue(order_id.startswith("Order #"))
        self.assertIn("Laptop", self.driver.page_source)

    # Functionalities 9: View Order Confirmation
    def test_view_order_confirmation(self):
        """Test order confirmation page"""
        self.login("admin", "admin123")
        add_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Add to Cart"]')
        add_buttons[0].click()  # Add Laptop
        
        self.driver.find_element(By.LINK_TEXT, "View Cart").click()
        self.wait.until(EC.url_contains('/cart'))
        
        self.driver.find_element(By.LINK_TEXT, "Proceed to Checkout").click()
        self.wait.until(EC.url_contains('/checkout'))
        
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Test Street")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("Visa 1234 5678 9012 3456")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        
        self.wait.until(EC.url_contains('/confirm/'))
        order_summary = self.driver.find_element(By.TAG_NAME, 'table')
        self.assertTrue(order_summary.is_displayed())
        self.assertIn("Total", order_summary.text)

    # Functionalities 10: Navigate Back to Product Listing Page
    def test_navigate_back_to_products(self):
        """Test navigation back to products from confirmation"""
        self.login("admin", "admin123")
        add_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Add to Cart"]')
        add_buttons[0].click()  # Add Laptop
        
        self.driver.find_element(By.LINK_TEXT, "View Cart").click()
        self.wait.until(EC.url_contains('/cart'))
        
        self.driver.find_element(By.LINK_TEXT, "Proceed to Checkout").click()
        self.wait.until(EC.url_contains('/checkout'))
        
        self.driver.find_element(By.NAME, 'shipping_address').send_keys("123 Test Street")
        self.driver.find_element(By.NAME, 'payment_info').send_keys("Visa 1234 5678 9012 3456")
        self.driver.find_element(By.XPATH, '//button[text()="Confirm Order"]').click()
        
        self.wait.until(EC.url_contains('/confirm/'))
        self.driver.find_element(By.LINK_TEXT, "Continue Shopping").click()
        self.wait.until(EC.url_contains('/products'))
        self.assertIn("Products", self.driver.title)

if __name__ == '__main__':
    unittest.main()
