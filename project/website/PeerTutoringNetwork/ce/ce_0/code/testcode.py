import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestPeerTutoringNetwork(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8718/')

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

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_access_dashboard(self):
        # Functionalities 3: Test access to the dashboard
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_view_available_tutors(self):
        # Functionalities 4: Test viewing available tutors
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows available tutors
        tutors = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tutors), 0, "No tutors found.")

    def test_request_tutoring(self):
        # Functionalities 5: Test requesting tutoring
        self.fail("Not implemented")

    def test_access_profile_page(self):
        # Functionalities 6
        self.fail("Not implemented")

    def test_user_logout(self):
        # Functionalities 7: Test logging out
        self.login("admin", "admin123")

        # Click the Logout button
        self.fail("Not implemented")

    def test_contact_support(self):
        # Functionalities 8: Test contacting support
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Contact Support').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the contact form
        self.driver.find_element(By.NAME, 'name').send_keys("John Doe")
        self.driver.find_element(By.NAME, 'email').send_keys("john@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("Need help with my account")
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Dashboard
        self.assertIn("Dashboard", self.driver.title)

    def test_cancel_tutoring_request(self):
        # Functionalities 9
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
