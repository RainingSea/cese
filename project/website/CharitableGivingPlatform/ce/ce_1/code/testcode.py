import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCharitableGivingPlatform(unittest.TestCase):

    def setUp(self):
        # Start the web server and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/') 

    def tearDown(self):
        # Close the web driver session and terminate the server process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("user1", "user123")
        
        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        
        # Verify that the Registration Page has loaded
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
        self.login("user1", "user123")

        # Verify that the charity list is displayed
        charities_list = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(charities_list), 0, "No charities found.")

    def test_navigate_to_charity_details(self):
        # Functionalities 5: Test navigation to Charity Details Page
        self.login("user1", "user123")
        
        # Click the 'Details' button for the first charity
        self.driver.find_element(By.XPATH, '//button[text()="Details"]').click()
        
        # Verify that the Charity Details Page has loaded
        self.assertIn("Charity Details", self.driver.title)

    def test_view_contribution_history(self):
        # Functionalities 6: Test viewing contribution history
        self.login("user1", "user123")

        # Navigate to the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Dashboard').click()
        
        # Verify that the contribution history is displayed
        history = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(history), 0, "No contribution history found.")

    def test_donate_to_charity(self):
        # Functionalities 7: Test donating to a charity
        self.login("user1", "user123")
        
        # Click the 'Details' button for the first charity
        self.driver.find_element(By.XPATH, '//button[text()="Details"]').click()
        
        # Enter a valid donation amount and click donate
        self.driver.find_element(By.ID, 'amount').send_keys("10.0")
        self.driver.find_element(By.XPATH, '//button[text()="Donate"]').click()

        # Verify that a confirmation message is displayed
        self.assertIn("Donation processed", self.driver.page_source)

    def test_user_logout(self):
        # Functionalities 8: Test logging out
        self.login("user1", "user123")

        # Click the Logout button
        self.driver.find_element(By.XPATH, '//button[text()="Logout"]').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionalities 9: Test navigating back to Dashboard
        self.login("user1", "user123")

        # Click the 'Details' button for the first charity
        self.driver.find_element(By.XPATH, '//button[text()="Details"]').click()

        # Click the back button
        self.driver.back()

        # Verify that the user is back on the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

    def test_local_data_storage(self):
        # Functionalities 10: Test adding a new charity and refreshing
        self.login("user1", "user123")

        # Simulate adding a new charity (this would typically be done in the application)
        with open('charities.txt', 'a') as f:
            f.write("charity3|New Charity|A new charity for testing.\n")

        # Refresh the Dashboard Page
        self.driver.refresh()

        # Verify that the new charity appears in the charity list
        charities_list = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertIn("New Charity", [charity.text for charity in charities_list])

if __name__ == '__main__':
    unittest.main()
