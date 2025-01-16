import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestRemoteJobBoardApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        # time.sleep(2)  # Wait for the web app to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8075')

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
        # Test case 1: User Login
        self.login("admin", "pass123")
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Test case 2: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the login page to load

        self.assertIn("Login", self.driver.title)

    def test_navigating_home_page_after_login(self):
        # Test case 3: Navigating Home Page After Login
        self.login("admin", "pass123")
        self.assertIn("Home", self.driver.title)

    def test_browsing_job_listings(self):
        # Test case 4: Browsing Job Listings
        self.login("admin", "pass123")
        # No explicit "Browse Jobs" button, assuming home page shows job listings
        jobs = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(jobs), 0, "No job listings found.")

    def test_posting_a_new_job_listing(self):
        # Test case 5: Posting a New Job Listing
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Post a Job').click()
        time.sleep(1)  # Wait for the job posting page to load

        job_title = "Test Job"
        company_name = "Test Company"
        job_description = "This is a test job description."

        self.driver.find_element(By.NAME, 'title').send_keys(job_title)
        self.driver.find_element(By.NAME, 'company').send_keys(company_name)
        self.driver.find_element(By.NAME, 'description').send_keys(job_description)
        self.driver.find_element(By.XPATH, '//button[text()="Post Job"]').click()
        time.sleep(1)  # Wait for the home page to load

        self.assertIn(job_title, self.driver.page_source)

    def test_editing_user_profile(self):
        # Test case 6: Editing User Profile
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        # No actual editing functionality implemented, so this test will fail
        self.fail("Editing user profile functionality not implemented.")

    def test_applying_for_job_postings(self):
        # Test case 7: Applying for Job Postings
        self.login("admin", "pass123")
        apply_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Apply"]')
        if apply_buttons:
            apply_buttons[0].click()
            time.sleep(1)  # Wait for the application to process
            self.assertIn("Home", self.driver.title)
        else:
            self.fail("No jobs available to apply for.")

    def test_viewing_user_profile(self):
        # Test case 8: Viewing User Profile
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        self.assertIn("User Profile", self.driver.page_source)

    def test_logging_out(self):
        # Test case 9: Logging Out
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the login page to load

        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
