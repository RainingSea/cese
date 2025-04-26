import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCharitableGivingPlatform(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8137/')  # Access the login page

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
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
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

    def test_view_charities_on_dashboard(self):
        # Functionalities 4: View Charities on the Dashboard Page
        self.login("admin", "admin123")
        charities_list = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(charities_list), 0, "No charities found.")

    def test_navigate_to_charity_details(self):
        # Functionalities 5: Navigate to Charity Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Details').click()
        self.assertIn("Charity Details", self.driver.title)

    def test_view_contribution_history(self):
        # Functionalities 6: View Contribution History
        self.login("admin", "admin123")
        contributions = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(contributions), 0, "No contributions found.")

    def test_donate_to_charity(self):
        # Functionalities 7: Donate to a Charity
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Details').click()
        self.driver.find_element(By.NAME, 'amount').send_keys("25.00")
        self.driver.find_element(By.XPATH, '//button[text()="Donate"]').click()
        self.assertIn("Dashboard", self.driver.title)

    def test_user_logout(self):
        # Functionalities 8: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionalities 9: Navigate Back to Dashboard
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Details').click()
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        self.assertIn("Dashboard", self.driver.title)

    def test_local_data_storage(self):
        # Functionalities 10: Local Data Storage
        self.login("admin", "admin123")
        # Simulate adding a new charity (this would normally be done through the app)
        with open('charities.txt', 'a') as file:
            file.write("Charity D|New Mission|New Projects\n")
        self.driver.refresh()  # Refresh the dashboard to see the new charity
        charities_list = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertIn("Charity D", [charity.text for charity in charities_list])

if __name__ == '__main__':
    unittest.main()
