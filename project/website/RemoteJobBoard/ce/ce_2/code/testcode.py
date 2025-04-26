import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestRemoteJobBoardApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8236/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)  # Verify redirection to home page

    def test_registration(self):
        # Functionalities 2: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

    def test_navigate_home_after_login(self):
        # Functionalities 3: Navigating Home Page After Login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)  # Verify redirection to home page

    def test_browsing_job_listings(self):
        # Functionalities 4: Browsing Job Listings
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Post a Job').click()  # Navigate to job posting page
        self.assertIn("Post Job", self.driver.title)  # Verify navigation to job posting page

    def test_posting_new_job_listing(self):
        # Functionalities 5: Posting a New Job Listing
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Post a Job').click()

        # Enter valid job details
        self.driver.find_element(By.NAME, 'title').send_keys("Software Engineer")
        self.driver.find_element(By.NAME, 'company').send_keys("Tech Company")
        self.driver.find_element(By.NAME, 'description').send_keys("Develop and maintain software applications.")
        self.driver.find_element(By.XPATH, '//button[text()="Post Job"]').click()

        # Verify redirection to home page
        self.assertIn("Home", self.driver.title)

    def test_viewing_user_profile(self):
        # Functionalities 8: Viewing User Profile
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.assertIn("User Profile", self.driver.title)  # Verify profile page title

    def test_logout(self):
        # Functionalities 9: Logging Out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)  # Verify redirection to login page

if __name__ == '__main__':
    unittest.main()
