import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCharitableGivingPlatform(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the actual port

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_charities(self):
        # Functionalities 4: View Charities on the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Available Charities", self.driver.page_source)

    def test_navigate_to_charity_details(self):
        # Functionalities 5: Navigate to Charity Details Page
        self.login("admin", "admin123")
        # Assuming there's a button for charity details
        self.driver.find_element(By.XPATH, '//button[text()="Details"]').click()
        self.assertIn("Charity Details", self.driver.title)

    def test_view_contribution_history(self):
        # Functionalities 6: View Contribution History
        self.login("admin", "admin123")
        self.assertIn("Your Contribution History", self.driver.page_source)

    def test_donate_to_charity(self):
        # Functionalities 7: Donate to a Charity
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Details"]').click()
        donation_amount = "50"
        self.driver.find_element(By.ID, 'amount').send_keys(donation_amount)
        self.driver.find_element(By.XPATH, '//button[text()="Donate"]').click()
        self.assertIn("Donation processed", self.driver.page_source)  # Adjust based on actual confirmation message

    def test_logout(self):
        # Functionalities 8: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionalities 9: Navigate Back to Dashboard
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Details"]').click()
        self.driver.find_element(By.XPATH, '//button[text()="Back to Dashboard"]').click()
        self.assertIn("Available Charities", self.driver.page_source)

    def test_local_data_storage(self):
        # Functionalities 10: Local Data Storage
        self.login("admin", "admin123")
        # Simulate adding a new charity in local storage (this part would depend on how you add charities)
        # After adding, refresh the dashboard and check for the new charity
        self.driver.refresh()
        self.assertIn("New Charity", self.driver.page_source)  # Adjust based on actual charity name

if __name__ == '__main__':
    unittest.main()
