import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestPeerTutoringNetwork(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8390/')  # Accessing the login page

    def tearDown(self):
        # Close the web driver session and the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)  # Verify redirection to dashboard

    def test_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.get('http://localhost:8390/register')  # Navigate to registration page
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.NAME, 'email').send_keys("new_user@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

    def test_access_dashboard(self):
        # Functionalities 3: Test access to the dashboard after login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)  # Verify dashboard access

    def test_view_available_tutors(self):
        # Functionalities 4: Test viewing available tutors
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Tutors').click()
        self.assertIn("Available Tutors", self.driver.title)  # Verify tutors page access

    def test_request_tutoring(self):
        # Functionalities 5: Test requesting tutoring
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Request Tutoring').click()
        self.driver.find_element(By.NAME, 'subject').send_keys("Math")
        self.driver.find_element(By.NAME, 'details').send_keys("Need help with algebra.")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-10")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Request"]').click()

        # Verify redirection to dashboard
        self.assertIn("Dashboard", self.driver.title)

    def test_access_profile(self):
        # Functionalities 6: Test access to the profile page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.assertIn("User Profile", self.driver.title)  # Verify profile page access

    def test_logout(self):
        # Functionalities 7: Test user logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)  # Verify redirection to login page

    def test_contact_support(self):
        # Functionalities 8: Test contacting support
        self.driver.get('http://localhost:8390/contact')  # Navigate to contact page
        self.driver.find_element(By.NAME, 'name').send_keys("Test User")
        self.driver.find_element(By.NAME, 'email').send_keys("test@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("This is a test message.")
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()

        # Verify confirmation message (assuming there's a confirmation message)
        self.assertIn("Message sent successfully", self.driver.page_source)

    def test_cancel_tutoring_request(self):
        # Functionalities 9: Test canceling a tutoring request (not implemented)
        self.fail("Cancel tutoring request functionality not implemented")

if __name__ == '__main__':
    unittest.main()
