import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestRemoteJobBoardApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8406/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("user1", "user123")
        self.assertIn("Home", self.driver.title)  # Check if redirected to home page

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.get('http://localhost:8406/register')  # Navigate to registration page
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_navigate_home_after_login(self):
        # Functionalities 3: Test navigating home page after login
        self.login("user1", "user123")
        self.assertIn("Home", self.driver.title)  # Check if redirected to home page

    def test_browsing_job_listings(self):
        # Functionalities 4: Test browsing job listings
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Jobs').click()
        self.assertIn("Browse Jobs", self.driver.title)  # Check if job listings page is displayed

    def test_posting_new_job_listing(self):
        # Functionalities 5: Test posting a new job listing
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Post a Job').click()

        # Fill out the job posting form
        self.driver.find_element(By.NAME, 'title').send_keys("Test Job")
        self.driver.find_element(By.NAME, 'company').send_keys("Test Company")
        self.driver.find_element(By.NAME, 'description').send_keys("This is a test job description.")
        self.driver.find_element(By.XPATH, '//button[text()="Post Job"]').click()

        # Verify that the job is posted successfully
        self.assertIn("Home", self.driver.title)  # Check if redirected to home page

    def test_editing_user_profile(self):
        # Functionalities 6: Test editing user profile (not implemented in the codebase)
        self.fail("Editing user profile functionality not implemented")

    def test_applying_for_job_postings(self):
        # Functionalities 7: Test applying for job postings (not implemented in the codebase)
        self.fail("Applying for job postings functionality not implemented")

    def test_viewing_user_profile(self):
        # Functionalities 8: Test viewing user profile
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.assertIn("User Profile", self.driver.title)  # Check if profile page is displayed

    def test_logging_out(self):
        # Functionalities 9: Test logging out
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)  # Check if redirected to login page

if __name__ == '__main__':
    unittest.main()
