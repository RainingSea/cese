import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestShopPalApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8410/') 

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8410/register')
        
        # Verify Registration form is displayed
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8410/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8410/login')

        # Verify Login form is displayed
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Invalid login
        self.driver.get('http://localhost:8410/login')
        self.login("admin", "wrongpassword")
        self.assertIn("Login", self.driver.title)  # Should remain on login page

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_navigate_to_dashboard(self):
        # Functionality 8: Navigate back to Dashboard
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8410/dashboard')
        self.assertIn("Dashboard", self.driver.title)

    def test_view_product_information(self):
        # Functionality 5: View Detailed Product Information
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8410/dashboard')

        # Assuming there is a product to click on
        product_elements = self.driver.find_elements(By.TAG_NAME, 'li')  # Assuming products are listed as <li>
        if product_elements:
            product_elements[0].click()  # Click on the first product
            self.assertIn("Product", self.driver.title)  # Check if product details page is displayed

    def test_search_products(self):
        # Functionality 6: Search for Products
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8410/dashboard')

        # Assuming there is a search bar
        search_bar = self.driver.find_element(By.NAME, 'search')  # Assuming the search bar has a name attribute
        search_bar.send_keys("Product A")
        search_bar.submit()

        # Verify that search results are displayed
        self.assertIn("Product A", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
