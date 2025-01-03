import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the web application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        # Close the web driver and the application process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Welcome to Freelancer Marketplace", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Test user registration functionality
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

    def test_access_home_page_after_login(self):
        # Test accessing the home page after logging in
        self.login("admin", "admin123")
        self.assertIn("Welcome to Freelancer Marketplace", self.driver.page_source)

    def test_search_freelancers(self):
        # Test searching for freelancers
        self.login("admin", "admin123")
        search_query = "John Doe"
        search_box = self.driver.find_element(By.NAME, 'search')
        search_box.send_keys(search_query)
        search_box.submit()
        time.sleep(1)  # Wait for the search results to load
        self.assertIn("John Doe", self.driver.page_source)

    def test_view_freelancer_profiles(self):
        # Test viewing freelancer profiles
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Freelancer Details').click()
        time.sleep(1)  # Wait for the profile page to load
        self.assertIn("Freelancer Profile", self.driver.title)

    def test_manage_projects(self):
        # Test navigating to the project management page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage All Projects').click()
        time.sleep(1)  # Wait for the project management page to load
        self.assertIn("Project Management", self.driver.title)

    def test_create_new_project(self):
        # Test creating a new project
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage All Projects').click()
        time.sleep(1)  # Wait for the project management page to load

        project_name = "New Project"
        description = "This is a new project."
        freelancer_name = "John Doe"

        self.driver.find_element(By.NAME, 'project_name').send_keys(project_name)
        self.driver.find_element(By.NAME, 'description').send_keys(description)
        self.driver.find_element(By.NAME, 'freelancer').send_keys(freelancer_name)
        self.driver.find_element(By.XPATH, '//button[text()="Create Project"]').click()
        time.sleep(1)  # Wait for the project to be created

        self.assertIn("Project created successfully!", self.driver.page_source)

    def test_view_project_lists(self):
        # Test viewing project lists
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage All Projects').click()
        time.sleep(1)  # Wait for the project management page to load
        self.assertIn("Existing Projects", self.driver.page_source)

    def test_profile_management(self):
        # Test navigating to the profile management page
        self.fail("Profile management functionality is not implemented.")

    def test_update_user_profile(self):
        # Test updating the user profile
        self.fail("Updating user profile functionality is not implemented.")

if __name__ == '__main__':
    unittest.main()
