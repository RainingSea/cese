import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestPeerTutoringNetwork(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8392/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
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
        self.assertIn("Dashboard", self.driver.title)  # Expect to be redirected to the dashboard

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        
        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_access_dashboard(self):
        # Functionalities 3: Test access to the dashboard after login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)  # Expect to be on the dashboard

    def test_view_available_tutors(self):
        # Functionalities 4: Test viewing available tutors
        self.login("admin", "admin123")
        # Assuming there is a button with text "View Tutors"
        self.driver.find_element(By.LINK_TEXT, 'View Tutors').click()
        self.assertIn("Available Tutors", self.driver.title)  # Expect to see the tutors page

    def test_request_tutoring(self):
        # Functionalities 5: Test requesting tutoring
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Request Tutoring').click()

        # Fill out the tutoring request form
        self.driver.find_element(By.NAME, 'subject').send_keys("Math")
        self.driver.find_element(By.NAME, 'details').send_keys("Need help with calculus.")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-10")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify that a confirmation message is displayed
        self.assertIn("Request submitted successfully", self.driver.page_source)

    def test_access_profile_page(self):
        # Functionalities 6: Test access to the profile page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.assertIn("Profile", self.driver.title)  # Expect to see the profile page

    def test_user_logout(self):
        # Functionalities 7: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)  # Expect to be redirected to the login page

    def test_contact_support(self):
        # Functionalities 8: Test contacting support
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Contact Support').click()

        # Fill out the contact form
        self.driver.find_element(By.NAME, 'name').send_keys("Test User")
        self.driver.find_element(By.NAME, 'email').send_keys("test@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("This is a test message.")
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()

        # Verify that a confirmation message is displayed
        self.assertIn("Message sent successfully", self.driver.page_source)

    def test_cancel_tutoring_request(self):
        # Functionalities 9: Test canceling a tutoring request
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Cancel Request').click()
        self.assertIn("Dashboard", self.driver.title)  # Expect to return to the dashboard

if __name__ == '__main__':
    unittest.main()
