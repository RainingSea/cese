import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestPeerTutoringNetwork(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the Flask application
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        # Stop the Flask application
        cls.process.terminate()

    def setUp(self):
        # Initialize the webdriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8030/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the webdriver
        self.driver.quit()

    def login(self, username, password):
        """Helper method to perform login"""
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.url_contains('dashboard'))

    def test_1_user_login(self):
        """Functionalities 1: Test valid user login"""
        self.login("student1", "student123")
        self.assertIn("Dashboard", self.driver.title)
        self.assertEqual(self.driver.current_url, 'http://localhost:8030/dashboard')

    def test_2_user_registration(self):
        """Functionalities 2: Test user registration"""
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.wait.until(EC.title_contains('Register'))
        
        # Generate unique username to avoid conflicts
        username = f"testuser{int(time.time())}"
        password = "testpass123"
        email = f"{username}@example.com"
        
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.NAME, 'email').send_keys(email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        self.wait.until(EC.url_contains('dashboard'))
        self.assertIn("Dashboard", self.driver.title)

    def test_3_access_dashboard(self):
        """Functionalities 3: Test dashboard access after login"""
        self.login("student1", "student123")
        
        # Verify navigation options are present
        nav_links = self.driver.find_elements(By.CSS_SELECTOR, 'nav ul li a')
        self.assertGreater(len(nav_links), 0)
        self.assertTrue(any(link.text == 'View Tutors' for link in nav_links))
        self.assertTrue(any(link.text == 'Request Tutoring' for link in nav_links))

    def test_4_view_available_tutors(self):
        """Functionalities 4: Test viewing available tutors"""
        self.login("student1", "student123")
        self.driver.find_element(By.LINK_TEXT, 'View Tutors').click()
        self.wait.until(EC.title_contains('Tutors'))
        
        # Verify tutors are displayed
        tutors = self.driver.find_elements(By.CSS_SELECTOR, 'ul li h3')
        self.assertGreater(len(tutors), 0)
        tutor_names = [tutor.text for tutor in tutors]
        self.assertIn("John Smith", tutor_names)

    def test_5_request_tutoring(self):
        """Functionalities 5: Test submitting a tutoring request"""
        self.login("student1", "student123")
        self.driver.find_element(By.LINK_TEXT, 'Request Tutoring').click()
        self.wait.until(EC.title_contains('Request'))
        
        # Fill out the form
        self.driver.find_element(By.NAME, 'subject').send_keys("Math")
        self.driver.find_element(By.NAME, 'details').send_keys("Need help with algebra")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-12-15")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Request"]').click()
        
        self.wait.until(EC.url_contains('dashboard'))
        self.assertIn("Dashboard", self.driver.title)

    def test_6_access_profile_page(self):
        """Functionalities 6: Test accessing profile page"""
        self.login("student1", "student123")
        self.driver.find_element(By.LINK_TEXT, 'My Profile').click()
        self.wait.until(EC.title_contains('Profile'))
        
        # Verify profile information
        username = self.driver.find_element(By.XPATH, '//p[contains(text(), "Username:")]').text
        email = self.driver.find_element(By.XPATH, '//p[contains(text(), "Email:")]').text
        self.assertIn("student1", username)
        self.assertIn("student1@school.edu", email)

    def test_7_user_logout(self):
        """Functionalities 7: Test user logout"""
        self.login("student1", "student123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains('Login'))
        self.assertEqual(self.driver.current_url, 'http://localhost:8030/login')

    def test_8_contact_support(self):
        """Functionalities 8: Test contacting support"""
        self.login("student1", "student123")
        self.driver.find_element(By.LINK_TEXT, 'Contact Support').click()
        self.wait.until(EC.title_contains('Contact'))
        
        # Fill out the contact form
        self.driver.find_element(By.NAME, 'name').send_keys("Test User")
        self.driver.find_element(By.NAME, 'email').send_keys("test@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("This is a test message")
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()
        
        self.wait.until(EC.url_contains('dashboard'))
        self.assertIn("Dashboard", self.driver.title)

    def test_9_cancel_tutoring_request(self):
        """Functionalities 9: Test canceling tutoring request"""
        self.login("student1", "student123")
        self.driver.find_element(By.LINK_TEXT, 'Request Tutoring').click()
        self.wait.until(EC.title_contains('Request'))
        
        # Click cancel button
        self.driver.find_element(By.LINK_TEXT, 'Cancel').click()
        
        self.wait.until(EC.url_contains('dashboard'))
        self.assertIn("Dashboard", self.driver.title)

if __name__ == '__main__':
    unittest.main()
