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
        self.driver.get('http://localhost:8069')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Test case 1: User Login
        self.login("admin", "adminpass")
        self.assertIn("Home", self.driver.title)

    def test_navigate_to_registration(self):
        # Test case 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Test case 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        self.driver.find_element(By.ID, 'username').send_keys(new_username)
        self.driver.find_element(By.ID, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Login", self.driver.title)

    def test_access_home_page_after_login(self):
        # Test case 4: Accessing Home Page after Login
        self.login("admin", "adminpass")
        self.assertIn("Welcome to Freelancer Marketplace", self.driver.page_source)

    def test_searching_for_freelancers(self):
        # Test case 5: Searching for Freelancers
        self.login("admin", "adminpass")
        # Assuming there is a search field and button on the home page
        self.fail("Search functionality not implemented")

    def test_viewing_freelancer_profiles(self):
        # Test case 6: Viewing Freelancer Profiles
        self.login("admin", "adminpass")
        # Assuming there is a way to view freelancer profiles
        self.fail("Freelancer profile viewing not implemented")

    def test_managing_projects(self):
        # Test case 7: Managing Projects
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Project Management", self.driver.title)

    def test_creating_a_new_project(self):
        # Test case 8: Creating a New Project
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load

        self.driver.find_element(By.ID, 'name').send_keys("New Project")
        self.driver.find_element(By.ID, 'description').send_keys("New Project Description")
        self.driver.find_element(By.ID, 'freelancer').send_keys("John Doe")
        self.driver.find_element(By.XPATH, '//button[text()="Create Project"]').click()
        time.sleep(1)  # Wait for the project to be created

        self.assertIn("New Project", self.driver.page_source)

    def test_viewing_project_lists(self):
        # Test case 9: Viewing Project Lists
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Existing Projects", self.driver.page_source)

    def test_profile_management(self):
        # Test case 10: Profile Management
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Manage Profile').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Profile Management", self.driver.title)

    def test_updating_user_profile(self):
        # Test case 11: Updating the User Profile
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Manage Profile').click()
        time.sleep(1)  # Wait for the next page to load

        self.driver.find_element(By.ID, 'username').clear()
        self.driver.find_element(By.ID, 'username').send_keys("admin")
        self.driver.find_element(By.ID, 'password').send_keys("new_adminpass")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the profile to be updated

        self.assertIn("Profile Management", self.driver.title)

if __name__ == '__main__':
    unittest.main()
