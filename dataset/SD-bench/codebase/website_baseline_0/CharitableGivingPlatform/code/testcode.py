import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestCharitableGivingPlatform(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8526/')

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
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration_page(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_charities_on_dashboard(self):
        # Functionalities 4: Test viewing charities on the Dashboard Page
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows charities
        charities = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(charities), 0, "No charities found.")

    def test_navigate_to_charity_details_page(self):
        # Functionalities 5: Test navigation to Charity Details Page
        self.login("admin", "admin123")

        # Click on a charity link
        self.driver.find_element(By.LINK_TEXT, 'Charity A').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Charity Details Page has loaded
        self.assertIn("Charity A", self.driver.title)

    def test_view_contribution_history(self):
        # Functionalities 6: Test viewing contribution history
        self.fail("Not implemented")

    def test_donate_to_charity(self):
        # Functionalities 7: Test donating to a charity
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Charity A').click()
        time.sleep(1)  # Wait for the next page to load

        # Enter donation amount and submit
        self.driver.find_element(By.NAME, 'amount').send_keys('10')
        self.driver.find_element(By.XPATH, '//button[text()="Donate"]').click()
        time.sleep(1)  # Wait for the donation to process

        # Verify that the user is redirected to the Dashboard
        self.assertIn("Dashboard", self.driver.title)

    def test_user_logout(self):
        # Functionalities 8: Test user logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.fail("Not implemented")

    def test_navigate_back_to_dashboard(self):
        # Functionalities 9: Test navigating back to the Dashboard
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Charity A').click()
        time.sleep(1)  # Wait for the next page to load

        # Click the back link
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_local_data_storage(self):
        # Functionalities 10: Test local data storage
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
