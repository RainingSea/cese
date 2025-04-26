import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestPeerTutoringNetwork(unittest.TestCase):

    def setUp(self):
        # Start the server and initialize the webdriver
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)  # Expectation: Redirected to dashboard

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        
        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Fill in the registration form
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_access_dashboard(self):
        # Functionalities 3: Test access to dashboard after login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)  # Expectation: Dashboard is accessible

    def test_view_available_tutors(self):
        # Functionalities 4: Test viewing available tutors
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Tutors').click()
        
        # Verify that the tutors are displayed
        self.assertIn("Available Tutors", self.driver.page_source)

    def test_request_tutoring(self):
        # Functionalities 5: Test submitting a tutoring request
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Request Tutoring').click()

        # Fill out the tutoring request form
        self.driver.find_element(By.NAME, 'subject').send_keys("Math")
        self.driver.find_element(By.NAME, 'details').send_keys("Need help with calculus.")
        self.driver.find_element(By.NAME, 'preferred_date').send_keys("2023-10-15")
        self.driver.find_element(By.XPATH, '//input[@value="Submit Request"]').click()

        # Verify that the request was submitted successfully
        self.assertIn("Request submitted", self.driver.page_source)

    def test_access_profile_page(self):
        # Functionalities 6: Test access to profile page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        
        # Verify that the profile page shows the user's information
        self.assertIn("Username: User", self.driver.page_source)

    def test_user_logout(self):
        # Functionalities 7: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        
        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_contact_support(self):
        # Functionalities 8: Test contacting support
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Contact Us').click()

        # Fill out the contact form
        self.driver.find_element(By.NAME, 'name').send_keys("John Doe")
        self.driver.find_element(By.NAME, 'email').send_keys("john@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("Need assistance with the website.")
        self.driver.find_element(By.XPATH, '//input[@value="Send Message"]').click()

        # Verify that the message was sent successfully
        self.assertIn("Message sent", self.driver.page_source)

    def test_cancel_tutoring_request(self):
        # Functionalities 9: Test canceling a tutoring request
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Request Tutoring').click()
        
        # Simulate canceling the request (assuming a cancel button exists)
        self.driver.find_element(By.LINK_TEXT, 'Cancel').click()
        
        # Verify that the user is returned to the dashboard
        self.assertIn("Dashboard", self.driver.title)

if __name__ == '__main__':
    unittest.main()
