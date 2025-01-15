import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestPeerTutoringNetwork(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8675/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()

        # Fill in the registration form
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.NAME, 'email').send_keys("new_user@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

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
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Request Tutoring').click()

        # Fill out the tutoring request form
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'subject').send_keys("Physics")
        self.driver.find_element(By.NAME, 'details').send_keys("Need help with quantum mechanics")
        self.driver.find_element(By.NAME, 'preferred_date').send_keys("2023-11-10")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Request"]').click()

        # Verify that the user is redirected to the dashboard
        self.assertIn("Dashboard", self.driver.title)

    def test_access_profile_page(self):
        # Functionalities 6: Test access to the profile page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()

        # Verify that the Profile Page has loaded
        self.assertIn("Profile", self.driver.title)

    def test_user_logout(self):
        # Functionalities 7: Test user logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_contact_support(self):
        # Functionalities 8: Test contact support functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Contact Us').click()

        # Fill out the contact form
        self.driver.find_element(By.NAME, 'name').send_keys("Test User")
        self.driver.find_element(By.NAME, 'email').send_keys("test_user@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("This is a test message.")
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()

        # Verify that the Contact Page has loaded (no confirmation message implemented)
        self.assertIn("Contact Us", self.driver.title)

    def test_cancel_tutoring_request(self):
        # Functionalities 9: Test cancel tutoring request functionality
        self.fail("Cancel tutoring request functionality is not implemented.")

if __name__ == '__main__':
    unittest.main()
