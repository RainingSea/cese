import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8534')

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

        # Verify that the user is redirected to the home page
        self.assertIn("Home", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
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
        # Functionalities 4: Test accessing home page after login
        self.login("admin", "admin123")

        # Verify that the home page displays a welcome message
        self.assertIn("Welcome to Freelancer Marketplace", self.driver.page_source)

    def test_search_freelancers(self):
        # Functionalities 5: Test searching for freelancers
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8534/freelancer_profile')

        # Enter a valid freelancer name in the search field
        self.driver.find_element(By.NAME, 'search_query').send_keys("John Doe")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        # Verify that search results display freelancers matching the entered name
        self.assertIn("John Doe", self.driver.page_source)

    def test_view_freelancer_profiles(self):
        # Functionalities 6: Test viewing freelancer profiles
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8534/freelancer_profile')

        # Click on a freelancer's profile link
        self.driver.find_element(By.LINK_TEXT, 'John Doe').click()
        time.sleep(1)  # Wait for the profile page to load

        # Verify that the freelancer profile page displays their details
        self.assertIn("Expert in web development", self.driver.page_source)

    def test_manage_projects(self):
        # Functionalities 7: Test managing projects
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8534/project_management')

        # Verify that the project management page displays all projects
        self.assertIn("Manage Projects", self.driver.page_source)

    def test_create_new_project(self):
        # Functionalities 8: Test creating a new project
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8534/project_management')

        # Enter valid project details and submit
        self.driver.find_element(By.NAME, 'project_name').send_keys("New Project")
        self.driver.find_element(By.NAME, 'project_description').send_keys("Project Description")
        self.driver.find_element(By.NAME, 'freelancer_name').send_keys("John Doe")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the project to be created

        # Verify that the project is created successfully
        self.assertIn("New Project", self.driver.page_source)

    def test_view_project_lists(self):
        # Functionalities 9: Test viewing project lists
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8534/project_management')

        # Verify that the user is presented with a list of all available projects
        self.assertIn("Website Redesign", self.driver.page_source)

    def test_profile_management(self):
        # Functionalities 10: Test profile management
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8534/profile_management')

        # Verify that the user is presented with current profile details for editing
        self.assertIn("Edit Profile", self.driver.page_source)

    def test_update_user_profile(self):
        # Functionalities 11: Test updating the user profile
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8534/profile_management')

        # Update password and submit
        self.driver.find_element(By.NAME, 'password').send_keys("new_admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the profile to be updated

        # Verify that the profile is updated successfully
        self.assertIn("Home", self.driver.title)

if __name__ == '__main__':
    unittest.main()
