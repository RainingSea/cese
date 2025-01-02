import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestRemoteJobBoard(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web app to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8181')

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
        self.login("admin", "pass123")
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input registration details
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for redirection to login page

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

    def test_navigate_home_after_login(self):
        # Functionalities 3: Test navigating home page after login
        self.login("admin", "pass123")
        self.assertIn("Home", self.driver.title)

    def test_browsing_job_listings(self):
        # Functionalities 4: Test browsing job listings
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse All Jobs').click()
        time.sleep(1)  # Wait for the browse jobs page to load
        self.assertIn("Browse Jobs", self.driver.title)

    def test_posting_new_job_listing(self):
        # Functionalities 5: Test posting a new job listing
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Post a Job').click()
        time.sleep(1)  # Wait for the post job page to load

        job_title = "Test Job"
        company_name = "Test Company"
        job_description = "This is a test job description."

        # Fill out the job posting form
        self.driver.find_element(By.NAME, 'title').send_keys(job_title)
        self.driver.find_element(By.NAME, 'company').send_keys(company_name)
        self.driver.find_element(By.NAME, 'description').send_keys(job_description)
        self.driver.find_element(By.XPATH, '//button[text()="Post Job"]').click()
        time.sleep(1)  # Wait for redirection to home page

        # Verify that the job is posted
        self.assertIn(job_title, self.driver.page_source)

    def test_editing_user_profile(self):
        # Functionalities 6: Test editing user profile
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)  # Wait for the profile page to load
        self.driver.find_element(By.LINK_TEXT, 'Edit Profile').click()
        time.sleep(1)  # Wait for the edit profile page to load

        new_email = "updated_email@example.com"
        self.driver.find_element(By.NAME, 'email').clear()
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Update"]').click()
        time.sleep(1)  # Wait for redirection to profile page

        # Verify that the email is updated
        self.assertIn(new_email, self.driver.page_source)

    def test_applying_for_job_postings(self):
        # Functionalities 7: Test applying for job postings
        self.fail("Not implemented")

    def test_viewing_user_profile(self):
        # Functionalities 8: Test viewing user profile
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        # Verify that the profile page displays user information
        self.assertIn("admin", self.driver.page_source)
        self.assertIn("admin@example.com", self.driver.page_source)

    def test_logging_out(self):
        # Functionalities 9: Test logging out
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for redirection to login page

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
