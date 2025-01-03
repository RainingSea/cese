import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestRemoteJobBoard(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8142')

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
        # Test case for User Login
        self.login("user1", "user1pass")
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Test case for User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
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
        # Test case for Navigating Home Page After Login
        self.login("user1", "user1pass")
        self.assertIn("Home", self.driver.title)
        jobs = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(jobs), 0, "No job listings found.")

    def test_browsing_job_listings(self):
        # Test case for Browsing Job Listings
        self.login("user1", "user1pass")
        self.driver.find_element(By.LINK_TEXT, 'Browse Jobs').click()
        time.sleep(1)  # Wait for the job listings page to load

        self.assertIn("Browse Jobs", self.driver.title)
        jobs = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(jobs), 0, "No job listings found.")

    def test_posting_new_job_listing(self):
        # Test case for Posting a New Job Listing
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Post a Job').click()
        time.sleep(1)  # Wait for the job post page to load

        job_title = "Test Job"
        company_name = "Test Company"
        description = "This is a test job description."

        self.driver.find_element(By.NAME, 'title').send_keys(job_title)
        self.driver.find_element(By.NAME, 'company').send_keys(company_name)
        self.driver.find_element(By.NAME, 'description').send_keys(description)
        self.driver.find_element(By.XPATH, '//button[text()="Post Job"]').click()
        time.sleep(1)  # Wait for the home page to load

        self.assertIn("Home", self.driver.title)
        self.assertIn(job_title, self.driver.page_source)

    def test_editing_user_profile(self):
        # Test case for Editing User Profile
        self.login("user1", "user1pass")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        new_email = "updated_user1@example.com"
        self.driver.find_element(By.NAME, 'email').clear()
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the home page to load

        self.assertIn("Home", self.driver.title)

    def test_applying_for_job_postings(self):
        # Test case for Applying for Job Postings
        self.login("user1", "user1pass")
        self.driver.find_element(By.LINK_TEXT, 'Browse Jobs').click()
        time.sleep(1)  # Wait for the job listings page to load

        apply_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Apply"]')
        if apply_buttons:
            apply_buttons[0].click()
            time.sleep(1)  # Wait for the page to reload
            self.assertIn("Browse Jobs", self.driver.title)
        else:
            self.fail("No jobs available to apply for.")

    def test_viewing_user_profile(self):
        # Test case for Viewing User Profile
        self.login("user1", "user1pass")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        self.assertIn("User Profile", self.driver.title)
        self.assertIn("user1", self.driver.page_source)

    def test_logging_out(self):
        # Test case for Logging Out
        self.login("user1", "user1pass")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the login page to load

        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
