import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestShopPalApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8697/')

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

    def test_user_registration(self):
        # Test user registration functionality
        self.driver.get('http://localhost:8697/register')
        time.sleep(1)  # Wait for the registration page to load

        # Step: Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Expectation: The user is registered successfully, and a confirmation message is displayed
        self.assertIn("Login", self.driver.title)

        # Step: Attempt to register with an existing username
        self.driver.get('http://localhost:8697/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Expectation: An error message is displayed indicating that the username is already taken
        self.assertIn("Username already exists.", self.driver.page_source)

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "admin123")

        # Expectation: Access is granted, and the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Step: Enter an invalid username or password
        self.driver.get('http://localhost:8697/')
        self.login("admin", "wrongpassword")

        # Expectation: An error message is displayed indicating that the login credentials are incorrect
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_create_personalized_collections(self):
        # Test creating personalized collections
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Collections').click()
        time.sleep(1)  # Wait for the collection page to load

        # Step: Create a new collection by entering a collection name and saving it
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'product_name').send_keys("Product1")
        self.driver.find_element(By.XPATH, '//button[text()="Add to Collection"]').click()
        time.sleep(1)  # Wait for the action to complete

        # Expectation: The new collection appears in the user's list of collections
        self.assertIn("Added Product1 to your collection.", self.driver.page_source)

    def test_track_price_changes(self):
        # Test tracking price changes
        self.fail("not implemented")

    def test_view_detailed_product_information(self):
        # Test viewing detailed product information
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Search Products').click()
        time.sleep(1)  # Wait for the search page to load

        # Step: Search for a product using keywords
        self.driver.find_element(By.NAME, 'query').send_keys("Product1")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        # Expectation: A list of products matching the search criteria is displayed
        self.assertIn("Product1", self.driver.page_source)

        # Step: Click on a product to view its detailed information
        self.driver.find_element(By.LINK_TEXT, 'Product1').click()
        time.sleep(1)  # Wait for the product detail page to load

        # Expectation: The detailed product information is displayed
        self.assertIn("Description of Product1", self.driver.page_source)

    def test_search_for_products(self):
        # Test searching for products
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Search Products').click()
        time.sleep(1)  # Wait for the search page to load

        # Step: Enter a keyword related to a product and submit the search
        self.driver.find_element(By.NAME, 'query').send_keys("Product")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        # Expectation: A list of products related to the keyword is displayed
        self.assertIn("Product1", self.driver.page_source)

    def test_user_logout(self):
        # Test user logout functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the logout action to complete

        # Expectation: The user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Step: Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8697/dashboard')
        time.sleep(1)  # Wait for the redirection

        # Expectation: The user is redirected back to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Test navigating back to the dashboard
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Search Products').click()
        time.sleep(1)  # Wait for the search page to load

        # Step: Click on a product to view its detailed information
        self.driver.find_element(By.NAME, 'query').send_keys("Product1")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load
        self.driver.find_element(By.LINK_TEXT, 'Product1').click()
        time.sleep(1)  # Wait for the product detail page to load

        # Step: Click the back button to return to the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)  # Wait for the dashboard page to load

        # Expectation: The user is redirected back to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

    def test_receive_notifications_for_discounts(self):
        # Test receiving notifications for discounts
        self.fail("not implemented")

if __name__ == '__main__':
    unittest.main()
