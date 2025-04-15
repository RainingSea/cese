import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestSocialLearnApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8318/') 

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
        self.driver.get('http://localhost:8318/register')

        # Verify the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify registration success message
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8318/register')
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("Registration Failed", self.driver.page_source)

    def test_user_login(self):
        # Test user login functionality
        self.driver.get('http://localhost:8318/')

        # Verify the Login form is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify redirection to the Profile Page
        self.assertIn("Profile", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8318/')
        self.login("invalid_user", "invalid_pass")

        # Verify error message for incorrect credentials
        self.assertIn("Login Failed", self.driver.page_source)

    def test_user_profile_management(self):
        # Test user profile management functionality
        self.login("admin", "admin123")

        # Verify the Profile Page is displayed
        self.assertIn("Profile", self.driver.title)

        # Update the profile with new areas of interest
        self.driver.find_element(By.NAME, 'interests').clear()
        self.driver.find_element(By.NAME, 'interests').send_keys('math,science,technology')
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)

        # Verify profile update success
        self.assertIn("Profile", self.driver.title)

        # Attempt to update the profile with invalid data (e.g., empty fields)
        self.driver.find_element(By.NAME, 'interests').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)

        # Verify error message for invalid data
        self.assertIn("Profile", self.driver.title)

    def test_user_logout(self):
        # Test user logout functionality
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the Profile Page after logging out
        self.driver.get('http://localhost:8318/profile')
        self.assertIn("Login", self.driver.title)

    def test_functionality_not_implemented(self):
        # Placeholder for functionalities not implemented in the codebase
        self.fail("Functionality not implemented")

if __name__ == '__main__':
    unittest.main()
