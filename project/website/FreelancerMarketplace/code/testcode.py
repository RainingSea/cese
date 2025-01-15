import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8467/')

    def tearDown(self):
        # Close the web driver session and stop the web application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Test Case 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)

    def test_navigate_to_registration_page(self):
        # Test Case 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Test Case 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "test_user"
        new_password = "test_password"

        self.driver.find_element(By.ID, 'username').send_keys(new_username)
        self.driver.find_element(By.ID, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Login", self.driver.title)

    def test_access_home_page_after_login(self):
        # Test Case 4: Accessing Home Page after Login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)

    def test_searching_for_freelancers(self):
        # Test Case 5: Searching for Freelancers
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8467/freelancer_profile')
        self.assertIn("Freelancer Profiles", self.driver.title)

    def test_viewing_freelancer_profiles(self):
        # Test Case 6: Viewing Freelancer Profiles
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8467/freelancer_profile')
        self.assertIn("Freelancer Profiles", self.driver.title)

    def test_managing_projects(self):
        # Test Case 7: Managing Projects
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8467/project_management')
        self.assertIn("Project Management", self.driver.title)

    def test_creating_a_new_project(self):
        # Test Case 8: Creating a New Project
        self.fail("Creating a new project functionality is not implemented.")

    def test_viewing_project_lists(self):
        # Test Case 9: Viewing Project Lists
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8467/project_management')
        self.assertIn("Project Management", self.driver.title)

    def test_profile_management(self):
        # Test Case 10: Profile Management
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8467/profile_management')
        self.assertIn("Profile Management", self.driver.title)

    def test_updating_the_user_profile(self):
        # Test Case 11: Updating the User Profile
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8467/profile_management')
        new_password = "new_admin123"
        self.driver.find_element(By.ID, 'new_password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Update Password"]').click()
        time.sleep(1)  # Wait for the update to process
        self.assertIn("Profile Management", self.driver.title)

if __name__ == '__main__':
    unittest.main()
