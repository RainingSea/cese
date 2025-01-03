import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestRemoteJobBoard(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

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
        # Test case for user login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Test case for user registration
        self.driver.find_element(By.LINK_TEXT, "Register here").click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Login", self.driver.title)

    def test_navigating_home_page_after_login(self):
        # Test case for navigating home page after login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)

    def test_browsing_job_listings(self):
        # Test case for browsing job listings
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Browse All Jobs").click()
        time.sleep(1)  # Wait for the job listings page to load

        self.assertIn("Browse Jobs", self.driver.title)

    def test_posting_new_job_listing(self):
        # Test case for posting a new job listing
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/job_posting')
        time.sleep(1)  # Wait for the job posting page to load

        job_title = "Test Job"
        company_name = "Test Company"
        job_description = "This is a test job description."

        self.driver.find_element(By.NAME, 'title').send_keys(job_title)
        self.driver.find_element(By.NAME, 'company').send_keys(company_name)
        self.driver.find_element(By.NAME, 'description').send_keys(job_description)
        self.driver.find_element(By.XPATH, '//button[text()="Post Job"]').click()
        time.sleep(1)  # Wait for the home page to load

        self.assertIn("Home", self.driver.title)

    def test_editing_user_profile(self):
        # Test case for editing user profile
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Profile").click()
        time.sleep(1)  # Wait for the profile page to load

        new_email = "updated_admin@example.com"
        email_input = self.driver.find_element(By.NAME, 'email')
        email_input.clear()
        email_input.send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Update Email"]').click()
        time.sleep(1)  # Wait for the profile page to reload

        self.assertIn("Profile", self.driver.title)

    def test_applying_for_job_postings(self):
        # Test case for applying for job postings
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Browse All Jobs").click()
        time.sleep(1)  # Wait for the job listings page to load

        self.driver.find_element(By.XPATH, '//button[text()="Apply"]').click()
        time.sleep(1)  # Wait for the browse jobs page to reload

        self.assertIn("Browse Jobs", self.driver.title)

    def test_viewing_user_profile(self):
        # Test case for viewing user profile
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Profile").click()
        time.sleep(1)  # Wait for the profile page to load

        self.assertIn("Profile", self.driver.title)

    def test_logging_out(self):
        # Test case for logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        time.sleep(1)  # Wait for the login page to load

        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
