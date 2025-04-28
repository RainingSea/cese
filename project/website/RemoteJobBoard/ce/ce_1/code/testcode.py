import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestRemoteJobBoardApp(unittest.TestCase):

    def setUp(self):
        # Start the main application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8407/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        # Verify that the user is redirected to the home page
        self.assertIn("Home", self.driver.title)

    def test_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.get('http://localhost:8407/register')  # Navigate to registration page
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_navigate_home_after_login(self):
        # Functionalities 3: Test navigating to home page after login
        self.login("admin", "admin123")
        # Verify that the user is on the home page
        self.assertIn("Home", self.driver.title)

    def test_browse_jobs(self):
        # Functionalities 4: Test browsing job listings
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Jobs').click()
        # Verify that job listings are displayed
        self.assertIn("Job Listings", self.driver.page_source)

    def test_post_job(self):
        # Functionalities 5: Test posting a new job listing
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8407/post_job')  # Navigate to post job page

        job_title = "Software Engineer"
        job_company = "Tech Company"
        job_description = "Develop software applications."

        # Fill out the job posting form
        self.driver.find_element(By.NAME, 'title').send_keys(job_title)
        self.driver.find_element(By.NAME, 'company').send_keys(job_company)
        self.driver.find_element(By.NAME, 'description').send_keys(job_description)
        self.driver.find_element(By.XPATH, '//button[text()="Post Job"]').click()

        # Verify that the job is posted successfully
        self.assertIn("Job Listings", self.driver.page_source)

    def test_edit_user_profile(self):
        # Functionalities 6: Test editing user profile (not implemented)
        self.fail("Edit user profile functionality not implemented")

    def test_apply_for_job(self):
        # Functionalities 7: Test applying for job postings (not implemented)
        self.fail("Apply for job postings functionality not implemented")

    def test_view_user_profile(self):
        # Functionalities 8: Test viewing user profile (not implemented)
        self.fail("View user profile functionality not implemented")

    def test_logout(self):
        # Functionalities 9: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
