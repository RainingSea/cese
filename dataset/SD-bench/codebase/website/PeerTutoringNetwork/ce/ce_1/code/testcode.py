import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestPeerTutoringNetwork(unittest.TestCase):

    def setUp(self):
        # Start the application server
        self.process = subprocess.Popen(['python', 'main.py'])
        # Initialize the webdriver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8676/')

    def tearDown(self):
        # Close the web driver session and terminate the server process
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
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
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
        # Verify that the list of tutors is displayed
        tutors = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tutors), 0, "No tutors found.")

    def test_request_tutoring(self):
        # Functionalities 5: Test requesting tutoring
        self.fail("Not implemented")

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
        # Functionalities 8: Test contact support
        self.fail("Not implemented")

    def test_cancel_tutoring_request(self):
        # Functionalities 9: Test cancel tutoring request
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
