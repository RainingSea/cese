import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestRemoteJobBoard(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8192/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("user1", "password1")

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

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
        # Functionalities 3: Test navigating to the home page after login
        self.login("user1", "password1")

        # Verify that the Home Page shows featured job listings
        jobs = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(jobs), 0, "No job listings found on the home page.")

    def test_browsing_job_listings(self):
        # Functionalities 4: Test browsing job listings
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Browse All Jobs').click()
        time.sleep(1)  # Wait for the browse jobs page to load

        # Verify that the Browse Jobs Page shows all job listings
        jobs = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(jobs), 0, "No job listings found on the browse jobs page.")

    def test_posting_new_job_listing(self):
        # Functionalities 5: Test posting a new job listing
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Post a Job').click()
        time.sleep(1)  # Wait for the post job page to load

        job_title = "Test Job"
        company_name = "Test Company"
        job_description = "This is a test job description."

        # Fill out the new job form
        self.driver.find_element(By.NAME, 'title').send_keys(job_title)
        self.driver.find_element(By.NAME, 'company').send_keys(company_name)
        self.driver.find_element(By.NAME, 'description').send_keys(job_description)
        self.driver.find_element(By.XPATH, '//button[text()="Post Job"]').click()
        time.sleep(1)  # Wait for the job to be posted

        # Verify that the job is displayed on the Home Page
        self.assertIn(job_title, self.driver.page_source)

    def test_editing_user_profile(self):
        # Functionalities 6: Test editing user profile
        self.fail("Not implemented")

    def test_applying_for_job_postings(self):
        # Functionalities 7: Test applying for job postings
        self.fail("Not implemented")

    def test_viewing_user_profile(self):
        # Functionalities 8: Test viewing user profile
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        # Verify that the Profile Page displays user information
        self.assertIn("User Profile", self.driver.page_source)

    def test_logging_out(self):
        # Functionalities 9: Test logging out
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
