import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestRemoteJobBoard(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8042/login')
        time.sleep(2)  # Wait for the application to start

    def tearDown(self):
        # Close the web driver session and stop the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:8042/login')
        username_field = self.driver.find_element(By.NAME, 'username')
        password_field = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.XPATH, '//button[text()="Login"]')
        
        username_field.clear()
        password_field.clear()
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        time.sleep(1)  # Wait for the next page to load

    def test_1_user_login(self):
        """Functionalities 1: Test user login with valid credentials"""
        self.login("admin", "admin123")
        
        # Verify redirection to home page
        self.assertIn("Featured Jobs", self.driver.page_source)
        self.assertIn("Welcome, admin", self.driver.page_source)

    def test_2_user_registration(self):
        """Functionalities 2: Test user registration with new credentials"""
        self.driver.get('http://localhost:8042/register')
        
        # Generate unique username to avoid conflicts
        test_username = f"testuser_{int(time.time())}"
        test_password = "testpassword123"
        test_email = f"{test_username}@example.com"
        
        # Fill registration form
        self.driver.find_element(By.NAME, 'username').send_keys(test_username)
        self.driver.find_element(By.NAME, 'password').send_keys(test_password)
        self.driver.find_element(By.NAME, 'email').send_keys(test_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        
        # Verify redirection to home page after registration
        self.assertIn("Featured Jobs", self.driver.page_source)
        self.assertIn(f"Welcome, {test_username}", self.driver.page_source)

    def test_3_home_page_after_login(self):
        """Functionalities 3: Test home page display after login"""
        self.login("admin", "admin123")
        
        # Verify featured jobs are displayed
        job_cards = self.driver.find_elements(By.CLASS_NAME, 'job-card')
        self.assertTrue(len(job_cards) > 0, "No featured jobs displayed on home page")

    def test_4_browsing_job_listings(self):
        """Functionalities 4: Test browsing all job listings"""
        self.login("admin", "admin123")
        
        # Click on Browse All Jobs button
        self.driver.find_element(By.LINK_TEXT, 'Browse All Jobs').click()
        time.sleep(1)
        
        # Verify job listings page
        self.assertIn("All Job Listings", self.driver.page_source)
        job_items = self.driver.find_elements(By.CLASS_NAME, 'job-item')
        self.assertTrue(len(job_items) > 0, "No job listings displayed")

    def test_5_posting_new_job(self):
        """Functionalities 5: Test posting a new job listing"""
        self.login("admin", "admin123")
        
        # Navigate to post job page
        self.driver.find_element(By.LINK_TEXT, 'Post a Job').click()
        time.sleep(1)
        
        # Fill job posting form
        job_title = f"Test Job {int(time.time())}"
        self.driver.find_element(By.NAME, 'title').send_keys(job_title)
        self.driver.find_element(By.NAME, 'company').send_keys("Test Company")
        self.driver.find_element(By.NAME, 'description').send_keys("This is a test job description")
        self.driver.find_element(By.XPATH, '//button[text()="Post Job"]').click()
        time.sleep(1)
        
        # Verify job was posted by checking home page
        self.assertIn(job_title, self.driver.page_source)

    def test_6_editing_user_profile(self):
        """Functionalities 6: Test editing user profile"""
        # This functionality is not implemented in the codebase
        self.fail("Editing user profile functionality not implemented")

    def test_7_applying_for_job(self):
        """Functionalities 7: Test applying for a job"""
        self.login("user1", "password1")
        
        # Navigate to jobs page
        self.driver.find_element(By.LINK_TEXT, 'Browse All Jobs').click()
        time.sleep(1)
        
        # Apply for the first job
        apply_buttons = self.driver.find_elements(By.LINK_TEXT, 'Apply')
        if len(apply_buttons) > 0:
            apply_buttons[0].click()
            time.sleep(1)
            
            # Verify application was successful by checking profile
            self.driver.find_element(By.LINK_TEXT, 'Profile').click()
            time.sleep(1)
            self.assertIn("Applied Jobs", self.driver.page_source)
        else:
            self.fail("No jobs available to apply for")

    def test_8_viewing_user_profile(self):
        """Functionalities 8: Test viewing user profile"""
        self.login("user1", "password1")
        
        # Navigate to profile page
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)
        
        # Verify profile information is displayed
        self.assertIn("Your Profile", self.driver.page_source)
        self.assertIn("Username: user1", self.driver.page_source)
        self.assertIn("Email: user1@example.com", self.driver.page_source)

    def test_9_logging_out(self):
        """Functionalities 9: Test logging out"""
        self.login("admin", "admin123")
        
        # Click logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        
        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)
        self.assertIn("Don't have an account?", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
