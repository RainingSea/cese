import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web app to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8130')

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
        # Test case for user login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)

    def test_navigate_to_registration(self):
        # Test case for navigating to the registration page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Test case for user registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Login", self.driver.title)

    def test_access_home_page_after_login(self):
        # Test case for accessing the home page after login
        self.login("admin", "admin123")
        self.assertIn("Welcome to Freelancer Marketplace", self.driver.page_source)

    def test_searching_for_freelancers(self):
        # Test case for searching freelancers
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'search').send_keys("user1")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load
        self.assertIn("user1", self.driver.page_source)

    def test_viewing_freelancer_profiles(self):
        # Test case for viewing freelancer profiles
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'search').send_keys("user1")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load
        self.driver.find_element(By.LINK_TEXT, 'user1').click()
        time.sleep(1)  # Wait for the profile page to load
        self.assertIn("Freelancer Profile: user1", self.driver.page_source)

    def test_managing_projects(self):
        # Test case for managing projects
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage All Projects').click()
        time.sleep(1)  # Wait for the manage projects page to load
        self.assertIn("Manage Projects", self.driver.title)

    def test_creating_new_project(self):
        # Test case for creating a new project
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage All Projects').click()
        time.sleep(1)  # Wait for the manage projects page to load

        self.driver.find_element(By.NAME, 'project_name').send_keys("New Project")
        self.driver.find_element(By.NAME, 'description').send_keys("New Project Description")
        self.driver.find_element(By.NAME, 'assigned_freelancer').send_keys("user1")
        self.driver.find_element(By.XPATH, '//button[text()="Create Project"]').click()
        time.sleep(1)  # Wait for the project to be created

        self.assertIn("New Project", self.driver.page_source)

    def test_viewing_project_lists(self):
        # Test case for viewing project lists
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage All Projects').click()
        time.sleep(1)  # Wait for the manage projects page to load
        self.assertIn("Existing Projects:", self.driver.page_source)

    def test_profile_management(self):
        # Test case for profile management
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile Management').click()
        time.sleep(1)  # Wait for the profile management page to load
        self.assertIn("Profile Management", self.driver.title)

    def test_updating_user_profile(self):
        # Test case for updating the user profile
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile Management').click()
        time.sleep(1)  # Wait for the profile management page to load

        new_username = "admin_updated"
        self.driver.find_element(By.NAME, 'username').clear()
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the profile to be updated

        self.assertIn("Home", self.driver.title)

if __name__ == '__main__':
    unittest.main()
