import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestRemoteJobBoardApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8234/')  # Use the port from main.py

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
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
        self.assertIn("Home", self.driver.title)  # Check if redirected to home page

    def test_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.get('http://localhost:8234/register')
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
        self.assertIn("Home", self.driver.title)  # Check if redirected to home page

    def test_browse_job_listings(self):
        # Functionalities 4: Test browsing job listings
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Jobs').click()
        self.assertIn("Job Listings", self.driver.title)  # Check if job listings page is displayed

    def test_post_new_job_listing(self):
        # Functionalities 5: Test posting a new job listing
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Post a Job').click()

        # Fill out the job posting form
        self.driver.find_element(By.NAME, 'title').send_keys("Software Engineer")
        self.driver.find_element(By.NAME, 'company').send_keys("Tech Company")
        self.driver.find_element(By.NAME, 'description').send_keys("Develop and maintain software applications.")
        self.driver.find_element(By.XPATH, '//button[text()="Post Job"]').click()

        # Verify that the job is posted by checking the job listings page
        self.driver.find_element(By.LINK_TEXT, 'Browse Jobs').click()
        self.assertIn("Software Engineer", self.driver.page_source)  # Check if job is listed

    def test_edit_user_profile(self):
        # Functionalities 6: Test editing user profile
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8234/profile')

        # Simulate editing the profile (this functionality is not implemented in the codebase)
        self.fail("Editing user profile functionality not implemented")

    def test_apply_for_job_postings(self):
        # Functionalities 7: Test applying for job postings
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Jobs').click()
        
        # Simulate applying for a job (this functionality is not implemented in the codebase)
        self.fail("Applying for job postings functionality not implemented")

    def test_view_user_profile(self):
        # Functionalities 8: Test viewing user profile
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8234/profile')
        self.assertIn("Username: admin", self.driver.page_source)  # Check if username is displayed

    def test_logout(self):
        # Functionalities 9: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)  # Check if redirected to login page

if __name__ == '__main__':
    unittest.main()
