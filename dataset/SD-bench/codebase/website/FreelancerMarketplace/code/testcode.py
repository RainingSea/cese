import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestWebApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/login')

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
        self.login("valid_user", "valid_password")

        # Verify that the user is redirected to the home page
        self.assertIn("Welcome", self.driver.page_source)

    def test_navigate_to_registration_page(self):
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
        self.login("valid_user", "valid_password")

        # Verify that the home page displays a welcome message
        self.assertIn("Welcome", self.driver.page_source)

    def test_search_for_freelancers(self):
        # Functionalities 5: Test searching for freelancers
        self.login("valid_user", "valid_password")

        # Enter a freelancer name in the search field
        self.driver.find_element(By.NAME, 'search').send_keys("Freelancer Name")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        # Verify that search results are displayed
        self.assertIn("Freelancer Name", self.driver.page_source)

    def test_view_freelancer_profiles(self):
        # Functionalities 6: Test viewing freelancer profiles
        self.login("valid_user", "valid_password")

        # Click on the "View Freelancer Details" button
        self.driver.find_element(By.XPATH, '//button[text()="View Freelancer Details"]').click()
        time.sleep(1)  # Wait for the profile page to load

        # Verify that the freelancer profile page is displayed
        self.assertIn("Freelancer Details", self.driver.page_source)

    def test_manage_projects(self):
        # Functionalities 7: Test managing projects
        self.login("valid_user", "valid_password")

        # Click on the "Manage All Projects" button
        self.driver.find_element(By.XPATH, '//button[text()="Manage All Projects"]').click()
        time.sleep(1)  # Wait for the project management page to load

        # Verify that the project management page is displayed
        self.assertIn("All Projects", self.driver.page_source)

    def test_create_new_project(self):
        # Functionalities 8: Test creating a new project
        self.login("valid_user", "valid_password")

        # Navigate to the project creation page
        self.driver.find_element(By.LINK_TEXT, 'Create New Project').click()
        time.sleep(1)  # Wait for the page to load

        # Enter project details
        self.driver.find_element(By.NAME, 'project_name').send_keys("New Project")
        self.driver.find_element(By.NAME, 'description').send_keys("Project Description")
        self.driver.find_element(By.NAME, 'freelancer').send_keys("Freelancer Name")
        self.driver.find_element(By.XPATH, '//button[text()="Create Project"]').click()
        time.sleep(1)  # Wait for the confirmation message

        # Verify that the project is created successfully
        self.assertIn("Project created successfully", self.driver.page_source)

    def test_view_project_lists(self):
        # Functionalities 9: Test viewing project lists
        self.login("valid_user", "valid_password")

        # Navigate to the project listing page
        self.driver.find_element(By.LINK_TEXT, 'Project List').click()
        time.sleep(1)  # Wait for the page to load

        # Verify that the project list is displayed
        self.assertIn("Project List", self.driver.page_source)

    def test_profile_management(self):
        # Functionalities 10: Test profile management
        self.login("valid_user", "valid_password")

        # Navigate to the profile management page
        self.driver.find_element(By.LINK_TEXT, 'Profile Management').click()
        time.sleep(1)  # Wait for the page to load

        # Verify that the profile management page is displayed
        self.assertIn("Profile Details", self.driver.page_source)

        # Update profile details
        self.driver.find_element(By.NAME, 'username').clear()
        self.driver.find_element(By.NAME, 'username').send_keys("updated_user")
        self.driver.find_element(By.NAME, 'email').clear()
        self.driver.find_element(By.NAME, 'email').send_keys("updated_email@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the confirmation message

        # Verify that the profile is updated successfully
        self.assertIn("Profile updated successfully", self.driver.page_source)

    def test_updating_user_profile(self):
        # Functionalities 11: Test updating the user profile
        self.login("valid_user", "valid_password")

        # Navigate to the profile management page
        self.driver.find_element(By.LINK_TEXT, 'Profile Management').click()
        time.sleep(1)  # Wait for the page to load

        # Update user details
        self.driver.find_element(By.NAME, 'username').clear()
        self.driver.find_element(By.NAME, 'username').send_keys("updated_user")
        self.driver.find_element(By.NAME, 'email').clear()
        self.driver.find_element(By.NAME, 'email').send_keys("updated_email@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the confirmation message

        # Verify that the profile is updated successfully
        self.assertIn("Profile updated successfully", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
