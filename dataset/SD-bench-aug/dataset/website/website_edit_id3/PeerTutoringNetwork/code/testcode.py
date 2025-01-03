import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestPeerTutoringNetwork(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8152')

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
        # Test case for user login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_user_registration(self):
        # Test case for user registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.NAME, 'email').send_keys("new_user@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the login page to load

        self.assertIn("Login", self.driver.title)

    def test_access_dashboard(self):
        # Test case for accessing the dashboard
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_view_available_tutors(self):
        # Test case for viewing available tutors
        self.login("admin", "admin123")
        tutors = self.driver.find_elements(By.XPATH, '//h2[text()="Available Tutors"]/following-sibling::ul/li')
        self.assertGreater(len(tutors), 0, "No tutors found.")

    def test_request_tutoring(self):
        # Test case for requesting tutoring
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'subject').send_keys("Physics")
        self.driver.find_element(By.NAME, 'details').send_keys("Need help with quantum mechanics.")
        self.driver.find_element(By.NAME, 'preferred_date').send_keys("2023-11-01")
        self.driver.find_element(By.XPATH, '//button[text()="Request Tutoring"]').click()
        time.sleep(1)  # Wait for the request to be processed

        requests = self.driver.find_elements(By.XPATH, '//h2[text()="Your Tutoring Requests"]/following-sibling::ul/li')
        self.assertGreater(len(requests), 0, "Tutoring request not found.")

    def test_access_profile_page(self):
        # Test case for accessing the profile page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        self.assertIn("Profile", self.driver.title)

    def test_user_logout(self):
        # Test case for user logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the login page to load

        self.assertIn("Login", self.driver.title)

    def test_contact_support(self):
        # Test case for contacting support
        self.driver.find_element(By.LINK_TEXT, 'Contact').click()
        time.sleep(1)  # Wait for the contact page to load

        self.driver.find_element(By.NAME, 'name').send_keys("Test User")
        self.driver.find_element(By.NAME, 'email').send_keys("test_user@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("This is a test message.")
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()
        time.sleep(1)  # Wait for the message to be sent

        self.assertIn("Login", self.driver.title)

    def test_cancel_tutoring_request(self):
        # Test case for canceling a tutoring request
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//h2[text()="Your Tutoring Requests"]/following-sibling::ul/li/form/button[text()="Cancel"]').click()
        time.sleep(1)  # Wait for the request to be canceled

        requests = self.driver.find_elements(By.XPATH, '//h2[text()="Your Tutoring Requests"]/following-sibling::ul/li')
        self.assertEqual(len(requests), 0, "Tutoring request was not canceled.")

if __name__ == '__main__':
    unittest.main()
