import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestRemoteJobBoard(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8041/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.url_contains('home'))

    def test_1_user_login(self):
        """Functionalities 1: User Login"""
        self.login("admin", "admin123")
        self.assertIn("Welcome", self.driver.page_source)
        self.assertIn("admin", self.driver.page_source)

    def test_2_user_registration(self):
        """Functionalities 2: User Registration"""
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.title_contains("Register"))
        
        # Generate unique username for each test run
        username = f"testuser{int(time.time())}"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys("testpass123")
        self.driver.find_element(By.NAME, 'email').send_keys(f"{username}@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        self.wait.until(EC.title_contains("Home"))
        self.assertIn(username, self.driver.page_source)

    def test_3_home_page_after_login(self):
        """Functionalities 3: Navigating Home Page After Login"""
        self.login("admin", "admin123")
        self.assertIn("Featured Jobs", self.driver.page_source)
        jobs = self.driver.find_elements(By.XPATH, '//ul/li')
        self.assertGreater(len(jobs), 0)

    def test_4_browsing_job_listings(self):
        """Functionalities 4: Browsing Job Listings"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Jobs').click()
        self.wait.until(EC.title_contains("Browse Jobs"))
        
        jobs = self.driver.find_elements(By.XPATH, '//ul/li')
        self.assertGreater(len(jobs), 0)
        self.assertIn("Python Developer", self.driver.page_source)
        self.assertIn("Web Designer", self.driver.page_source)

    def test_5_posting_new_job(self):
        """Functionalities 5: Posting a New Job Listing"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Post Job').click()
        self.wait.until(EC.title_contains("Post Job"))
        
        job_title = f"Test Job {int(time.time())}"
        self.driver.find_element(By.NAME, 'title').send_keys(job_title)
        self.driver.find_element(By.NAME, 'company').send_keys("Test Company")
        self.driver.find_element(By.NAME, 'description').send_keys("Test job description")
        self.driver.find_element(By.XPATH, '//button[text()="Post Job"]').click()
        
        self.wait.until(EC.title_contains("Home"))
        self.assertIn(job_title, self.driver.page_source)

    def test_6_editing_user_profile(self):
        """Functionalities 6: Editing User Profile"""
        # This functionality is not implemented in the codebase
        self.fail("Editing user profile functionality not implemented")

    def test_7_applying_for_jobs(self):
        """Functionalities 7: Applying for Job Postings"""
        self.login("john", "password123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Jobs').click()
        self.wait.until(EC.title_contains("Browse Jobs"))
        
        # Find and click the first Apply link
        apply_links = self.driver.find_elements(By.LINK_TEXT, 'Apply')
        if len(apply_links) > 0:
            apply_links[0].click()
            self.wait.until(EC.title_contains("Browse Jobs"))
            
            # Verify application by checking profile
            self.driver.find_element(By.LINK_TEXT, 'Profile').click()
            self.wait.until(EC.title_contains("Profile"))
            self.assertIn("Applied Jobs", self.driver.page_source)
        else:
            self.fail("No jobs available to apply for")

    def test_8_viewing_user_profile(self):
        """Functionalities 8: Viewing User Profile"""
        self.login("john", "password123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.wait.until(EC.title_contains("Profile"))
        
        self.assertIn("User Information", self.driver.page_source)
        self.assertIn("john", self.driver.page_source)
        self.assertIn("john@example.com", self.driver.page_source)
        self.assertIn("Applied Jobs", self.driver.page_source)

    def test_9_logging_out(self):
        """Functionalities 9: Logging Out"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains("Login"))
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
