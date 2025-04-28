import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestCharitableGivingPlatform(unittest.TestCase):

    def setUp(self):
        # Start the server and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8080/') 

    def tearDown(self):
        # Close the web driver session and terminate the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_charities_on_dashboard(self):
        # Functionalities 4: Test viewing charities on the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Available Charities", self.driver.page_source)

    def test_navigate_to_charity_details(self):
        # Functionalities 5: Test navigation to Charity Details Page
        self.login("admin", "admin123")
        # Assuming there is a button or link for charity details
        self.driver.find_element(By.LINK_TEXT, 'Charity1 Details').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Charity Details", self.driver.title)

    def test_view_contribution_history(self):
        # Functionalities 6: Test viewing contribution history
        self.login("admin", "admin123")
        self.assertIn("Your Contributions", self.driver.page_source)

    def test_donate_to_charity(self):
        # Functionalities 7: Test donating to a charity
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Charity1 Details').click()
        time.sleep(1)  # Wait for the next page to load

        donation_amount = "50"
        self.driver.find_element(By.NAME, 'amount').send_keys(donation_amount)
        self.driver.find_element(By.XPATH, '//input[@value="Donate"]').click()
        time.sleep(1)  # Wait for the donation to process

        # Verify donation confirmation (assuming a confirmation message appears)
        self.assertIn("Donation processed successfully", self.driver.page_source)

    def test_user_logout(self):
        # Functionalities 8: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionalities 9: Test navigating back to Dashboard
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Charity1 Details').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Available Charities", self.driver.page_source)

    def test_local_data_storage(self):
        # Functionalities 10: Test adding a new charity and refreshing
        self.fail("Not implemented")  # Placeholder for future implementation

if __name__ == '__main__':
    unittest.main()
