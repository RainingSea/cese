import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestPeerTutoringNetwork(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        # Close the web driver and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:5000')  # Go to login page
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Test user login functionality
        self.login("user1", "password1")
        self.assertIn("Welcome to Your Dashboard", self.driver.page_source)

    def test_user_registration(self):
        # Test user registration functionality
        self.driver.get('http://localhost:5000/register')
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Fill in the registration form
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

    def test_access_dashboard(self):
        # Test accessing the dashboard after login
        self.login("user1", "password1")
        self.assertIn("Welcome to Your Dashboard", self.driver.page_source)

    def test_view_available_tutors(self):
        # Test viewing available tutors
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'View Tutors').click()
        time.sleep(1)  # Wait for the tutors page to load
        self.assertIn("Available Tutors", self.driver.page_source)

    def test_request_tutoring(self):
        # Test requesting tutoring
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Request Tutoring').click()
        time.sleep(1)  # Wait for the request tutoring page to load

        subject = "Mathematics"
        details = "Need help with calculus."
        preferred_date = "2023-12-31"

        # Fill out the tutoring request form
        self.driver.find_element(By.NAME, 'subject').send_keys(subject)
        self.driver.find_element(By.NAME, 'details').send_keys(details)
        self.driver.find_element(By.NAME, 'preferred_date').send_keys(preferred_date)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Request"]').click()
        time.sleep(1)  # Wait for the request to be processed

        # Verify redirection to dashboard
        self.assertIn("Welcome to Your Dashboard", self.driver.page_source)

    def test_access_profile_page(self):
        # Test accessing the profile page
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'View Profile').click()
        time.sleep(1)  # Wait for the profile page to load
        self.assertIn("User Profile", self.driver.page_source)

    def test_user_logout(self):
        # Test logging out
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the logout to process
        self.assertIn("Login", self.driver.title)

    def test_contact_support(self):
        # Test contacting support
        self.driver.get('http://localhost:5000/contact')
        time.sleep(1)  # Wait for the contact page to load

        name = "Test User"
        email = "test_user@example.com"
        message = "This is a test message."

        # Fill out the contact form
        self.driver.find_element(By.NAME, 'name').send_keys(name)
        self.driver.find_element(By.NAME, 'email').send_keys(email)
        self.driver.find_element(By.NAME, 'message').send_keys(message)
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()
        time.sleep(1)  # Wait for the message to be sent

        # Verify redirection to dashboard
        self.assertIn("Welcome to Your Dashboard", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
