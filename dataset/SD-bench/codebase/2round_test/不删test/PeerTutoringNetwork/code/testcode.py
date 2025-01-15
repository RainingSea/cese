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
        self.driver.get('http://localhost:8063/')  # Access the login page

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
        # Functionalities 1: Test user login functionality
        self.login("user1", "pass123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

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
        self.login("user1", "pass123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_view_available_tutors(self):
        # Functionalities 4: Test viewing available tutors
        self.login("user1", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'View Tutors').click()
        time.sleep(1)  # Wait for the tutors page to load

        # Verify that the list of tutors is displayed
        tutors = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tutors), 0, "No tutors found.")

    def test_request_tutoring(self):
        # Functionalities 5: Test requesting tutoring
        self.login("user1", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Request Tutoring').click()
        time.sleep(1)  # Wait for the request tutoring page to load

        # Fill out the tutoring request form
        self.driver.find_element(By.NAME, 'subject').send_keys("Chemistry")
        self.driver.find_element(By.NAME, 'details').send_keys("Need help with organic chemistry.")
        self.driver.find_element(By.NAME, 'preferred_date').send_keys("2023-11-01")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Request"]').click()
        time.sleep(1)  # Wait for the dashboard to load

        # Verify that the user is redirected to the dashboard
        self.assertIn("Dashboard", self.driver.title)

    def test_access_profile_page(self):
        # Functionalities 6: Test access to the profile page
        self.login("user1", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        # Verify that the profile page shows the user's username and email
        self.assertIn("user1", self.driver.page_source)
        self.assertIn("user1@example.com", self.driver.page_source)

    def test_user_logout(self):
        # Functionalities 7: Test user logout
        self.login("user1", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the login page to load

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_contact_support(self):
        # Functionalities 8: Test contact support
        self.login("user1", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Contact Support').click()
        time.sleep(1)  # Wait for the contact us page to load

        # Fill out the contact form
        self.driver.find_element(By.NAME, 'name').send_keys("Test User")
        self.driver.find_element(By.NAME, 'email').send_keys("testuser@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("This is a test message.")
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()
        time.sleep(1)  # Wait for the dashboard to load

        # Verify that the user is redirected to the dashboard
        self.assertIn("Dashboard", self.driver.title)

    def test_cancel_tutoring_request(self):
        # Functionalities 9: Test cancel tutoring request
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
