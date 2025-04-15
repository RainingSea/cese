import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestSocialLearnApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8317/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and terminate the web application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Registration", self.driver.title)

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        self.assertIn("Registration", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")
        self.assertIn("Profile", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8317/')
        self.login("invalid_user", "invalid_pass")
        self.assertIn("Login", self.driver.title)

    def test_user_profile_management(self):
        # Login successfully and navigate to the Profile Page
        self.login("admin", "admin123")
        self.assertIn("Profile", self.driver.title)

        # Update the profile with new areas of interest and save changes
        self.driver.find_element(By.NAME, 'interests').clear()
        self.driver.find_element(By.NAME, 'interests').send_keys('coding,reading,swimming')
        self.driver.find_element(By.XPATH, '//button[text()="Update Interests"]').click()
        time.sleep(1)
        self.assertIn("Profile", self.driver.title)

    def test_join_study_groups(self):
        # Functionality not implemented in the codebase
        self.fail("Join Study Groups functionality not implemented")

    def test_share_and_access_educational_resources(self):
        # Functionality not implemented in the codebase
        self.fail("Share and Access Educational Resources functionality not implemented")

    def test_messaging_in_study_groups(self):
        # Functionality not implemented in the codebase
        self.fail("Messaging in Study Groups functionality not implemented")

    def test_user_logout(self):
        # Login and then logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the Profile Page after logging out
        self.driver.get('http://localhost:8317/profile')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality not implemented in the codebase
        self.fail("Navigate Back to Dashboard functionality not implemented")

    def test_view_educational_resource_details(self):
        # Functionality not implemented in the codebase
        self.fail("View Educational Resource Details functionality not implemented")

if __name__ == '__main__':
    unittest.main()
