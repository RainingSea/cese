import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCharitableGivingPlatform(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8376/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_charities_on_dashboard(self):
        # Functionalities 4: Test viewing charities on the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Charities", self.driver.page_source)

    def test_navigate_to_charity_details(self):
        # Functionalities 5: Test navigation to Charity Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//a[contains(text(), "Details")]').click()
        self.assertIn("Charity Details", self.driver.title)

    def test_donate_to_charity(self):
        # Functionalities 7: Test donating to a charity
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//a[contains(text(), "Details")]').click()
        self.driver.find_element(By.NAME, 'amount').send_keys("50")
        self.driver.find_element(By.XPATH, '//button[text()="Donate"]').click()
        self.assertIn("Dashboard", self.driver.title)

    def test_user_logout(self):
        # Functionalities 8: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Logout"]').click()
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionalities 9: Test navigating back to Dashboard
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//a[contains(text(), "Details")]').click()
        self.driver.find_element(By.LINK_TEXT, 'Back').click()
        self.assertIn("Charities", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
