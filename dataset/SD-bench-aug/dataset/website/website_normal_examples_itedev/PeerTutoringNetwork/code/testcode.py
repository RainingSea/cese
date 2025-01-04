import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestPeerTutoringNetwork(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/login')

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
        self.login("testuser", "password123")
        self.assertIn("User Dashboard", self.driver.title)

    def test_user_registration(self):
        # Test case for user registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        self.driver.find_element(By.NAME, 'username').send_keys("newuser")
        self.driver.find_element(By.NAME, 'password').send_keys("newpassword")
        self.driver.find_element(By.NAME, 'email').send_keys("newuser@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Login", self.driver.title)

    def test_access_dashboard(self):
        # Test case for accessing the dashboard
        self.login("testuser", "password123")
        self.assertIn("User Dashboard", self.driver.title)

    def test_view_available_tutors(self):
        # Test case for viewing available tutors
        self.login("testuser", "password123")
        self.driver.find_element(By.XPATH, '//button[text()="View Tutors"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Available Tutors", self.driver.title)

    def test_request_tutoring(self):
        # Test case for requesting tutoring
        self.login("testuser", "password123")
        self.driver.find_element(By.XPATH, '//button[text()="Request Tutoring"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.driver.find_element(By.NAME, 'subject').send_keys("Math")
        self.driver.find_element(By.NAME, 'details').send_keys("Need help with calculus.")
        self.driver.find_element(By.NAME, 'preferred_date').send_keys("2023-10-10")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Request"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("User Dashboard", self.driver.title)

    def test_access_profile_page(self):
        # Test case for accessing the profile page
        self.login("testuser", "password123")
        self.driver.find_element(By.XPATH, '//button[text()="View Profile"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("User Profile", self.driver.title)

    def test_user_logout(self):
        # Test case for user logout
        self.login("testuser", "password123")
        self.driver.find_element(By.XPATH, '//button[text()="Logout"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Login", self.driver.title)

    def test_contact_support(self):
        # Test case for contacting support
        self.driver.find_element(By.LINK_TEXT, 'Contact Support').click()
        time.sleep(1)  # Wait for the next page to load

        self.driver.find_element(By.NAME, 'name').send_keys("Test User")
        self.driver.find_element(By.NAME, 'email').send_keys("testuser@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("This is a test message.")
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("User Dashboard", self.driver.title)

    def test_cancel_tutoring_request(self):
        # Test case for canceling a tutoring request
        self.login("testuser", "password123")
        self.driver.find_element(By.XPATH, '//button[text()="Request Tutoring"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.driver.find_element(By.XPATH, '//button[text()="Cancel"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("User Dashboard", self.driver.title)

if __name__ == '__main__':
    unittest.main()
