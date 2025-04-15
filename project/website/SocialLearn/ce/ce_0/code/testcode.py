import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestSocialLearnApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8316/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and stop the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.get('http://localhost:8316/register')
        self.assertIn("Registration", self.driver.title)

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.ID, 'username').send_keys('new_user')
        self.driver.find_element(By.ID, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify registration success message
        self.assertIn("Registration successful! Please log in.", self.driver.page_source)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8316/register')
        self.driver.find_element(By.ID, 'username').send_keys('admin')
        self.driver.find_element(By.ID, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("Registration Failed: Username already exists.", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8316/')
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")
        self.assertNotIn("Login", self.driver.title)  # Check that user is redirected

        # Enter an invalid username or password
        self.driver.get('http://localhost:8316/')
        self.login("invalid_user", "wrong_password")
        self.assertIn("Login", self.driver.title)  # Check that user is not redirected

    def test_user_profile_management(self):
        # Login and navigate to the Profile Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8316/profile')
        self.assertIn("Profile of admin", self.driver.page_source)

        # Update the profile with new areas of interest
        self.driver.find_element(By.ID, 'interests').clear()
        self.driver.find_element(By.ID, 'interests').send_keys('math, science, technology')
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)

        # Verify profile update success message
        self.assertIn("Profile updated successfully!", self.driver.page_source)

    def test_user_logout(self):
        # Login and then logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the Profile Page
        self.driver.get('http://localhost:8316/profile')
        self.assertIn("Login", self.driver.title)  # Check that access is denied

    # Additional tests for functionalities not implemented
    def test_join_study_groups(self):
        self.fail("Functionality not implemented")

    def test_share_and_access_educational_resources(self):
        self.fail("Functionality not implemented")

    def test_messaging_in_study_groups(self):
        self.fail("Functionality not implemented")

    def test_navigate_back_to_dashboard(self):
        self.fail("Functionality not implemented")

    def test_view_educational_resource_details(self):
        self.fail("Functionality not implemented")

if __name__ == '__main__':
    unittest.main()
