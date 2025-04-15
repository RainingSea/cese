import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestRemoteJobBoard(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8306/')

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
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_navigating_home_page_after_login(self):
        # Functionalities 3: Test navigating home page after login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)

    def test_browsing_job_listings(self):
        # Functionalities 4: Test browsing job listings
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Jobs').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Job Listings Page has loaded
        self.assertIn("Job Listings", self.driver.title)

    def test_posting_a_new_job_listing(self):
        # Functionalities 5: Test posting a new job listing
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Post a Job').click()
        time.sleep(1)  # Wait for the next page to load

        # Enter job details
        self.driver.find_element(By.NAME, 'title').send_keys("Test Job")
        self.driver.find_element(By.NAME, 'company').send_keys("Test Company")
        self.driver.find_element(By.NAME, 'description').send_keys("Test Description")
        self.driver.find_element(By.XPATH, '//button[text()="Post Job"]').click()
        time.sleep(1)  # Wait for the job to be posted

        # Verify the job is posted successfully
        self.assertIn("Home", self.driver.title)

    def test_editing_user_profile(self):
        # Functionalities 6: Test editing user profile
        self.fail("not implemented")

    def test_applying_for_job_postings(self):
        # Functionalities 7: Test applying for job postings
        self.fail("not implemented")

    def test_viewing_user_profile(self):
        # Functionalities 8: Test viewing user profile
        self.fail("not implemented")

    def test_logging_out(self):
        # Functionalities 9: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
