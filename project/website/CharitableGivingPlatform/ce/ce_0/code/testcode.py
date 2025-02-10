import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestCharitableGivingPlatform(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8593/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
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

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
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
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_charities_on_dashboard(self):
        # Functionalities 4: Test viewing charities on the Dashboard Page
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows charities
        charities = self.driver.find_elements(By.XPATH, '//ul/li/a')
        self.assertGreater(len(charities), 0, "No charities found.")

    def test_navigate_to_charity_details(self):
        # Functionalities 5: Test navigation to Charity Details Page
        self.login("admin", "admin123")

        # Click on a charity link to navigate to its details page
        charity_link = self.driver.find_element(By.XPATH, '//ul/li/a')
        charity_name = charity_link.text
        charity_link.click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Charity Details Page has loaded
        self.assertIn(charity_name, self.driver.title)

    def test_view_contribution_history(self):
        # Functionalities 6: Test viewing contribution history
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows contributions
        contributions = self.driver.find_elements(By.XPATH, '//h2[text()="Your Contributions"]/following-sibling::ul/li')
        self.assertGreater(len(contributions), 0, "No contributions found.")

    def test_donate_to_charity(self):
        # Functionalities 7: Test donating to a charity
        self.fail("not implemented")

    def test_user_logout(self):
        # Functionalities 8: Test user logout functionality
        self.fail("not implemented")

    def test_navigate_back_to_dashboard(self):
        # Functionalities 9: Test navigation back to the Dashboard Page
        self.fail("not implemented")

    def test_local_data_storage(self):
        # Functionalities 10: Test local data storage
        self.fail("not implemented")

if __name__ == '__main__':
    unittest.main()
