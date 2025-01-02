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
        self.driver.get('http://localhost:8165')

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
        self.login("admin", "adminpass")

        # Verify that the Dashboard Page has loaded
        self.assertIn("User Dashboard", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
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
        self.assertIn("Login", self.driver.page_source)

    def test_access_dashboard(self):
        # Functionalities 3: Test access to the dashboard
        self.login("admin", "adminpass")

        # Verify that the Dashboard Page has loaded
        self.assertIn("User Dashboard", self.driver.page_source)

    def test_view_available_tutors(self):
        # Functionalities 4: Test viewing available tutors
        self.login("admin", "adminpass")

        # Verify that the Dashboard Page shows available tutors
        tutors = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tutors), 0, "No tutors found.")

    def test_request_tutoring(self):
        # Functionalities 5: Test requesting tutoring
        self.login("admin", "adminpass")

        # Fill out the tutoring request form
        self.driver.find_element(By.NAME, 'subject').send_keys("Math")
        self.driver.find_element(By.NAME, 'details').send_keys("Need help with calculus.")
        self.driver.find_element(By.NAME, 'preferred_date').send_keys("2023-10-10")
        self.driver.find_element(By.XPATH, '//button[text()="Request Tutoring"]').click()
        time.sleep(1)  # Wait for the request to be processed

        # Verify that the request is submitted successfully
        self.assertIn("User Dashboard", self.driver.page_source)

    def test_access_profile_page(self):
        # Functionalities 6: Test access to the profile page
        self.login("admin", "adminpass")
        self.driver.get('http://localhost:8165/profile')
        time.sleep(1)  # Wait for the profile page to load

        # Verify that the profile page shows the user's username and email
        self.assertIn("admin", self.driver.page_source)
        self.assertIn("admin@example.com", self.driver.page_source)

    def test_user_logout(self):
        # Functionalities 7: Test user logout
        self.login("admin", "adminpass")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.page_source)

    def test_contact_support(self):
        # Functionalities 8: Test contact support functionality
        self.driver.get('http://localhost:8165/contact')
        time.sleep(1)  # Wait for the contact page to load

        # Fill out the contact form
        self.driver.find_element(By.NAME, 'name').send_keys("John Doe")
        self.driver.find_element(By.NAME, 'email').send_keys("john.doe@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("I need help with my account.")
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()
        time.sleep(1)  # Wait for the message to be processed

        # Verify that the message is sent successfully
        self.assertIn("Login", self.driver.page_source)

    def test_cancel_tutoring_request(self):
        # Functionalities 9: Test cancel tutoring request functionality
        self.fail("Cancel tutoring request functionality not implemented")

if __name__ == '__main__':
    unittest.main()
