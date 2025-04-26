import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestRemoteJobBoardApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8235/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: User Login
        self.login("user1", "user123")
        self.assertIn("Home", self.driver.title)  # Expectation: Redirected to home page

    def test_registration(self):
        # Functionalities 2: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        
        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_navigate_home_after_login(self):
        # Functionalities 3: Navigating Home Page After Login
        self.login("user1", "user123")
        self.assertIn("Home", self.driver.title)  # Expectation: Home page is displayed

    def test_browsing_job_listings(self):
        # Functionalities 4: Browsing Job Listings
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'View All Jobs').click()
        self.assertIn("Job Listings", self.driver.title)  # Expectation: Job listings page is displayed

    def test_posting_new_job_listing(self):
        # Functionalities 5: Posting a New Job Listing
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Post a Job').click()

        job_title = "New Software Engineer"
        job_company = "New Tech Company"
        job_description = "Develop new software applications."

        # Fill out the job posting form
        self.driver.find_element(By.NAME, 'title').send_keys(job_title)
        self.driver.find_element(By.NAME, 'company').send_keys(job_company)
        self.driver.find_element(By.NAME, 'description').send_keys(job_description)
        self.driver.find_element(By.XPATH, '//button[text()="Post Job"]').click()

        # Verify that the job is posted successfully
        self.assertIn("Job Listings", self.driver.title)  # Expectation: Redirected to job listings page

    def test_edit_user_profile(self):
        # Functionalities 6: Editing User Profile
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()

        new_email = "updated_user@example.com"
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Update"]').click()

        # Verify that the profile updates successfully
        self.assertIn("User Profile", self.driver.title)  # Expectation: Profile page is displayed

    def test_applying_for_job_postings(self):
        # Functionalities 7: Applying for Job Postings
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'View All Jobs').click()

        # Apply for the first job listing
        self.driver.find_element(By.XPATH, '//button[text()="Apply"]').click()

        # Verify that the application is submitted successfully
        self.assertIn("Job Listings", self.driver.title)  # Expectation: Redirected to job listings page

    def test_viewing_user_profile(self):
        # Functionalities 8: Viewing User Profile
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.assertIn("User Profile", self.driver.title)  # Expectation: Profile page is displayed

    def test_logout(self):
        # Functionalities 9: Logging Out
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)  # Expectation: Redirected to login page

if __name__ == '__main__':
    unittest.main()
