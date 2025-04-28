import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestPeerTutoringNetwork(unittest.TestCase):

    def setUp(self):
        # Start the server and initialize the webdriver
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8080/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.get('http://localhost:8080/register')  # Navigate to registration page
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.NAME, 'email').send_keys("new_user@example.com")
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        self.assertIn("Login", self.driver.title)  # Check if redirected to login page

    def test_access_dashboard(self):
        # Functionalities 3: Test access to the dashboard after login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_view_available_tutors(self):
        # Functionalities 4: Test viewing available tutors
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Tutors').click()
        self.assertIn("Available Tutors", self.driver.page_source)

    def test_request_tutoring(self):
        # Functionalities 5: Test submitting a tutoring request
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Request Tutoring').click()
        self.driver.find_element(By.NAME, 'subject').send_keys("Math")
        self.driver.find_element(By.NAME, 'details').send_keys("Need help with calculus.")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-25")
        self.driver.find_element(By.XPATH, '//input[@value="Submit Request"]').click()
        self.assertIn("Dashboard", self.driver.title)  # Check if redirected to dashboard

    def test_access_profile_page(self):
        # Functionalities 6: Test access to the profile page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.assertIn("User Profile", self.driver.page_source)

    def test_contact_support(self):
        # Functionalities 8: Test contacting support
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Contact Us').click()
        self.driver.find_element(By.NAME, 'name').send_keys("Test User")
        self.driver.find_element(By.NAME, 'email').send_keys("test@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("This is a test message.")
        self.driver.find_element(By.XPATH, '//input[@value="Send Message"]').click()
        self.assertIn("Dashboard", self.driver.title)  # Check if redirected to dashboard

    def test_cancel_tutoring_request(self):
        # Functionalities 9: Test canceling a tutoring request
        self.login("admin", "admin123")
        # Assuming there is a way to cancel a request, this is a placeholder
        self.fail("Cancel tutoring request functionality not implemented.")

if __name__ == '__main__':
    unittest.main()
