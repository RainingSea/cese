import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestPeerTutoringNetwork(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8029/login')
        time.sleep(2)  # Wait for the application to start

    def tearDown(self):
        # Close the web driver session and stop the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        """Functionalities 1: Test valid user login"""
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)
        self.assertIn("Welcome, admin!", self.driver.page_source)

    def test_user_registration(self):
        """Functionalities 2: Test user registration"""
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        
        # Fill registration form
        self.driver.find_element(By.NAME, 'username').send_keys("newuser")
        self.driver.find_element(By.NAME, 'password').send_keys("newpass123")
        self.driver.find_element(By.NAME, 'email').send_keys("new@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        
        # Verify redirect to login page
        self.assertIn("Login", self.driver.title)

    def test_access_dashboard(self):
        """Functionalities 3: Test dashboard access after login"""
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)
        
        # Verify navigation options are present
        nav_links = self.driver.find_elements(By.CSS_SELECTOR, 'nav ul li a')
        self.assertTrue(len(nav_links) > 0, "Navigation options not found")

    def test_view_available_tutors(self):
        """Functionalities 4: Test viewing available tutors"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Tutors').click()
        time.sleep(1)
        
        # Verify tutors are displayed
        tutors = self.driver.find_elements(By.CSS_SELECTOR, 'ul li strong')
        self.assertTrue(len(tutors) > 0, "No tutors displayed")

    def test_request_tutoring(self):
        """Functionalities 5: Test submitting a tutoring request"""
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Request Tutoring').click()
        time.sleep(1)
        
        # Fill request form
        self.driver.find_element(By.NAME, 'subject').send_keys("Math")
        self.driver.find_element(By.NAME, 'details').send_keys("Need help with algebra")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Request"]').click()
        time.sleep(1)
        
        # Verify redirect to dashboard
        self.assertIn("Dashboard", self.driver.title)

    def test_access_profile_page(self):
        """Functionalities 6: Test accessing profile page"""
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'My Profile').click()
        time.sleep(1)
        
        # Verify profile information is displayed
        username = self.driver.find_element(By.XPATH, '//p[contains(., "Username:")]')
        email = self.driver.find_element(By.XPATH, '//p[contains(., "Email:")]')
        self.assertTrue(username.is_displayed() and email.is_displayed())

    def test_user_logout(self):
        """Functionalities 7: Test user logout"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        
        # Verify redirect to login page
        self.assertIn("Login", self.driver.title)

    def test_contact_support(self):
        """Functionalities 8: Test contacting support"""
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Contact Us').click()
        time.sleep(1)
        
        # Fill contact form
        self.driver.find_element(By.NAME, 'name').send_keys("Test User")
        self.driver.find_element(By.NAME, 'email').send_keys("test@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("This is a test message")
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()
        time.sleep(1)
        
        # Verify redirect to dashboard
        self.assertIn("Dashboard", self.driver.title)

    def test_cancel_tutoring_request(self):
        """Functionalities 9: Test canceling tutoring request"""
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Request Tutoring').click()
        time.sleep(1)
        
        # Click cancel button
        self.driver.find_element(By.LINK_TEXT, 'Cancel').click()
        time.sleep(1)
        
        # Verify redirect to dashboard
        self.assertIn("Dashboard", self.driver.title)

if __name__ == '__main__':
    unittest.main()
