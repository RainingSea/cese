import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import subprocess

class TestPeerTutoringApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8028/')
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)

    def test_user_login(self):
        """Functionalities 1: Test valid user login"""
        self.login("student1", "student123")
        self.assertIn("Dashboard", self.driver.title)
        self.assertIn("Welcome, student1!", self.driver.page_source)

    def test_user_registration(self):
        """Functionalities 2: Test user registration"""
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        
        username = "new_user_" + str(int(time.time()))
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys("newpass123")
        self.driver.find_element(By.NAME, 'email').send_keys(f"{username}@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        
        self.assertIn("Login", self.driver.title)

    def test_access_dashboard(self):
        """Functionalities 3: Test dashboard access after login"""
        self.login("student1", "student123")
        self.assertIn("Dashboard", self.driver.title)
        
        # Verify navigation options are present
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, "View Tutors").is_displayed())
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, "Make Request").is_displayed())
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, "View Profile").is_displayed())

    def test_view_available_tutors(self):
        """Functionalities 4: Test viewing available tutors"""
        self.login("student1", "student123")
        self.driver.find_element(By.LINK_TEXT, "View Tutors").click()
        time.sleep(1)
        
        self.assertIn("Available Tutors", self.driver.page_source)
        tutors_table = self.driver.find_element(By.TAG_NAME, "table")
        rows = tutors_table.find_elements(By.TAG_NAME, "tr")
        self.assertGreater(len(rows), 1)  # Header row + at least one tutor

    def test_request_tutoring(self):
        """Functionalities 5: Test submitting a tutoring request"""
        self.login("student1", "student123")
        self.driver.find_element(By.LINK_TEXT, "Make Request").click()
        time.sleep(1)
        
        # Fill out the request form
        select = Select(self.driver.find_element(By.ID, "tutor"))
        select.select_by_visible_text("tutor1 (Math, Physics)")
        
        self.driver.find_element(By.ID, "subject").send_keys("Math")
        self.driver.find_element(By.ID, "details").send_keys("Need help with calculus")
        self.driver.find_element(By.ID, "date").send_keys("2023-12-15")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Request"]').click()
        time.sleep(1)
        
        self.assertIn("Dashboard", self.driver.title)

    def test_access_profile_page(self):
        """Functionalities 6: Test accessing profile page"""
        self.login("student1", "student123")
        self.driver.find_element(By.LINK_TEXT, "View Profile").click()
        time.sleep(1)
        
        self.assertIn("Your Profile", self.driver.page_source)
        self.assertIn("student1", self.driver.page_source)
        self.assertIn("student1@school.edu", self.driver.page_source)

    def test_user_logout(self):
        """Functionalities 7: Test user logout"""
        self.login("student1", "student123")
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        time.sleep(1)
        
        self.assertIn("Login", self.driver.title)
        self.assertIn("Don't have an account?", self.driver.page_source)

    def test_contact_support(self):
        """Functionalities 8: Test contact support form"""
        self.driver.find_element(By.LINK_TEXT, "Contact").click()
        time.sleep(1)
        
        self.driver.find_element(By.NAME, "name").send_keys("Test User")
        self.driver.find_element(By.NAME, "email").send_keys("test@example.com")
        self.driver.find_element(By.NAME, "message").send_keys("This is a test message")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)
        
        success_message = self.driver.find_element(By.CLASS_NAME, "alert-success")
        self.assertTrue(success_message.is_displayed())

    def test_cancel_tutoring_request(self):
        """Functionalities 9: Test canceling tutoring request"""
        # This functionality isn't implemented in the UI according to the codebase
        # So we'll mark it as expected failure
        self.fail("Cancel tutoring request functionality not implemented in UI")

if __name__ == '__main__':
    unittest.main()
