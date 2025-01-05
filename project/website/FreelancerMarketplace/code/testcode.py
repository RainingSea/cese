import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8025')

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
        self.login("admin1", "pass123")
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
        # Test case for accessing home page after login
        self.login("admin1", "pass123")
        self.assertIn("Welcome to Freelancer Marketplace", self.driver.page_source)

    def test_search_freelancers(self):
        # Test case for searching freelancers
        self.fail("Not implemented")

    def test_view_freelancer_profiles(self):
        # Test case for viewing freelancer profiles
        self.fail("Not implemented")

    def test_manage_projects(self):
        # Test case for managing projects
        self.fail("Not implemented")

    def test_create_new_project(self):
        # Test case for creating a new project
        self.login("admin1", "pass123")
        self.driver.find_element(By.NAME, 'name').send_keys("New Project")
        self.driver.find_element(By.NAME, 'description').send_keys("Project Description")
        self.driver.find_element(By.NAME, 'freelancer').send_keys("Freelancer1")
        self.driver.find_element(By.XPATH, '//button[text()="Create Project"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the project is created successfully
        self.assertIn("Welcome to Freelancer Marketplace", self.driver.page_source)

    def test_view_project_lists(self):
        # Test case for viewing project lists
        self.fail("Not implemented")

    def test_profile_management(self):
        # Test case for profile management
        self.fail("Not implemented")

    def test_update_user_profile(self):
        # Test case for updating the user profile
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
