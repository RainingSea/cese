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
        # Initialize the webdriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8043/')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        # Terminate the Flask application
        self.process.terminate()

    def login(self, username, password):
        """Helper method to perform login"""
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        # Wait for page to load
        self.wait.until(EC.url_contains('home'))

    def test_user_login(self):
        """Functionalities 1: Test user login with valid credentials"""
        self.login("user1", "user123")
        # Verify redirection to home page
        self.assertIn("Welcome", self.driver.page_source)
        self.assertIn("user1", self.driver.page_source)

    def test_user_registration(self):
        """Functionalities 2: Test user registration with new credentials"""
        # Go to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.wait.until(EC.title_contains("Register"))
        
        # Fill registration form
        username = "newuser_" + str(int(time.time()))
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'email').send_keys(f"{username}@example.com")
        self.driver.find_element(By.NAME, 'password').send_keys("newpassword123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        # Verify redirection to home page after successful registration
        self.wait.until(EC.url_contains('home'))
        self.assertIn("Welcome", self.driver.page_source)

    def test_home_page_navigation(self):
        """Functionalities 3: Test navigation to home page after login"""
        self.login("user1", "user123")
        # Verify featured jobs are displayed
        jobs = self.driver.find_elements(By.CSS_SELECTOR, 'div[style*="border:1px solid #ccc"]')
        self.assertGreater(len(jobs), 0, "No featured jobs displayed")

    def test_browsing_job_listings(self):
        """Functionalities 4: Test browsing job listings"""
        self.login("user1", "user123")
        # Navigate to jobs page
        self.driver.find_element(By.LINK_TEXT, 'Jobs').click()
        self.wait.until(EC.title_contains("Jobs"))
        
        # Verify jobs are displayed
        jobs = self.driver.find_elements(By.CSS_SELECTOR, 'div[style*="border:1px solid #ccc"]')
        self.assertGreater(len(jobs), 0, "No jobs displayed")

    def test_posting_new_job(self):
        """Functionalities 5: Test posting a new job listing"""
        self.login("admin", "admin123")
        # Navigate to jobs page
        self.driver.find_element(By.LINK_TEXT, 'Jobs').click()
        self.wait.until(EC.title_contains("Jobs"))
        
        # Fill job posting form
        job_title = "Test Job " + str(int(time.time()))
        self.driver.find_element(By.NAME, 'title').send_keys(job_title)
        self.driver.find_element(By.NAME, 'company').send_keys("Test Company")
        self.driver.find_element(By.NAME, 'description').send_keys("Test job description")
        self.driver.find_element(By.XPATH, '//button[text()="Post Job"]').click()
        
        # Verify job appears in listings
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'//h3[contains(text(), "{job_title}")]')))

    def test_editing_user_profile(self):
        """Functionalities 6: Test editing user profile"""
        self.login("user1", "user123")
        # Navigate to profile page
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.wait.until(EC.title_contains("Profile"))
        
        # Edit email
        new_email = "newemail_" + str(int(time.time())) + "@example.com"
        email_field = self.driver.find_element(By.NAME, 'email')
        email_field.clear()
        email_field.send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Update"]').click()
        
        # Verify email was updated
        self.wait.until(EC.text_to_be_present_in_element_value((By.NAME, 'email'), new_email))

    def test_applying_for_job(self):
        """Functionalities 7: Test applying for a job"""
        self.login("user1", "user123")
        # Navigate to jobs page
        self.driver.find_element(By.LINK_TEXT, 'Jobs').click()
        self.wait.until(EC.title_contains("Jobs"))
        
        # Find and click the first apply button
        apply_buttons = self.driver.find_elements(By.XPATH, '//a[contains(@href, "/apply_job/")]')
        if len(apply_buttons) > 0:
            apply_buttons[0].click()
            # Verify we're still on jobs page after applying
            self.wait.until(EC.title_contains("Jobs"))
        else:
            self.fail("No jobs available to apply for")

    def test_viewing_user_profile(self):
        """Functionalities 8: Test viewing user profile"""
        self.login("user1", "user123")
        # Navigate to profile page
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.wait.until(EC.title_contains("Profile"))
        
        # Verify profile information is displayed
        self.assertIn("user1", self.driver.page_source)
        self.assertIn("user1@example.com", self.driver.page_source)
        # Check if applied jobs section exists
        self.assertTrue(self.driver.find_elements(By.XPATH, '//h2[text()="Your Applications"]'))

    def test_logging_out(self):
        """Functionalities 9: Test logging out"""
        self.login("user1", "user123")
        # Click logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains("Login"))
        
        # Verify we're back on login page
        self.assertIn("Login", self.driver.title)
        self.assertIn("Don't have an account", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
