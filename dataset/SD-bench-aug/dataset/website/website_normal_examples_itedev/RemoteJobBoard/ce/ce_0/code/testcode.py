import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestRemoteJobBoardApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the web application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()  # Terminate the Flask application

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Test user login functionality
        self.login("user1", "password1")
        self.assertIn("Home", self.driver.title)  # Expect to be redirected to home page

    def test_user_registration(self):
        # Test user registration functionality
        self.driver.get('http://localhost:5000/register')
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

    def test_navigate_home_after_login(self):
        # Test navigating to home page after login
        self.login("user1", "password1")
        self.assertIn("Home", self.driver.title)  # Expect to be on the home page

    def test_browsing_job_listings(self):
        # Test browsing job listings
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Browse All Jobs').click()
        time.sleep(1)  # Wait for the job listings page to load
        self.assertIn("All Job Listings", self.driver.title)  # Expect to be on job listings page

    def test_posting_new_job_listing(self):
        # Test posting a new job listing
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Post a Job').click()
        time.sleep(1)  # Wait for the job posting page to load

        job_title = "Test Job"
        job_company = "Test Company"
        job_description = "This is a test job description."

        # Fill out the job posting form
        self.driver.find_element(By.NAME, 'title').send_keys(job_title)
        self.driver.find_element(By.NAME, 'company').send_keys(job_company)
        self.driver.find_element(By.NAME, 'description').send_keys(job_description)
        self.driver.find_element(By.XPATH, '//button[text()="Post Job"]').click()
        time.sleep(1)  # Wait for the job to be posted

        # Verify that the job is displayed on the home page
        self.assertIn(job_title, self.driver.page_source)

    def test_editing_user_profile(self):
        # Test editing user profile
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        new_email = "updated_email@example.com"
        self.driver.find_element(By.NAME, 'email').clear()
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the profile to update

        # Verify that the updated email is displayed on the profile page
        self.assertIn(new_email, self.driver.page_source)

    def test_applying_for_job_postings(self):
        # Test applying for job postings
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Browse All Jobs').click()
        time.sleep(1)  # Wait for the job listings page to load

        # Apply for the first job listing
        self.driver.find_element(By.XPATH, '//button[text()="Apply"]').click()
        time.sleep(1)  # Wait for the application to be submitted

        # Verify that the application was submitted
        self.assertIn("Applied", self.driver.page_source)  # Assuming "Applied" appears on the profile

    def test_viewing_user_profile(self):
        # Test viewing user profile
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        # Verify that the profile displays the username and email
        self.assertIn("user1", self.driver.page_source)
        self.assertIn("user1@example.com", self.driver.page_source)

    def test_logging_out(self):
        # Test logging out
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the logout to complete

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
