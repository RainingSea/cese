import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestRemoteJobBoard(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8551')

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
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_navigating_home_page_after_login(self):
        # Functionalities 3: Test navigating to home page after login
        self.login("admin", "admin123")

        # Verify that the Home Page shows featured job listings
        self.assertIn("Featured Job Listings", self.driver.page_source)

    def test_browsing_job_listings(self):
        # Functionalities 4: Test browsing job listings
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Jobs').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Browse Jobs Page has loaded
        self.assertIn("Job Listings", self.driver.page_source)

    def test_posting_new_job_listing(self):
        # Functionalities 5: Test posting a new job listing
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Post a Job').click()
        time.sleep(1)  # Wait for the next page to load

        job_title = "Test Job"
        company_name = "Test Company"
        job_description = "This is a test job description."

        # Fill out the job posting form
        self.driver.find_element(By.NAME, 'title').send_keys(job_title)
        self.driver.find_element(By.NAME, 'company').send_keys(company_name)
        self.driver.find_element(By.NAME, 'description').send_keys(job_description)
        self.driver.find_element(By.XPATH, '//button[text()="Post Job"]').click()
        time.sleep(1)  # Wait for the job to be posted

        # Verify that the job is displayed on the Home Page
        self.assertIn(job_title, self.driver.page_source)

    def test_editing_user_profile(self):
        # Functionalities 6: Test editing user profile
        self.fail("not implemented")

    def test_applying_for_job_postings(self):
        # Functionalities 7: Test applying for job postings
        self.login("admin", "admin123")

        # Apply for the first job in the list
        self.driver.find_element(By.XPATH, '//form/button[text()="Apply"]').click()
        time.sleep(1)  # Wait for the application to be processed

        # Verify that the application is logged under the user's applied jobs
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)  # Wait for the profile page to load
        self.assertIn("Software Engineer", self.driver.page_source)

    def test_viewing_user_profile(self):
        # Functionalities 8: Test viewing user profile
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        # Verify that the user profile displays the username, email, and applied jobs
        self.assertIn("admin", self.driver.page_source)
        self.assertIn("admin@example.com", self.driver.page_source)

    def test_logging_out(self):
        # Functionalities 9: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
