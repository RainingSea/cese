import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8382/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Welcome to Freelancer Marketplace", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_access_home_page_after_login(self):
        # Functionalities 4: Test accessing home page after login
        self.login("admin", "admin123")
        self.assertIn("Welcome to Freelancer Marketplace", self.driver.page_source)

    def test_search_freelancers(self):
        # Functionalities 5: Test searching for freelancers
        self.login("admin", "admin123")
        search_query = "John Doe"
        self.driver.find_element(By.NAME, 'query').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that search results display freelancers matching the entered name
        self.assertIn("John Doe", self.driver.page_source)

    def test_view_freelancer_profiles(self):
        # Functionalities 6: Test viewing freelancer profiles
        self.login("admin", "admin123")
        search_query = "John Doe"
        self.driver.find_element(By.NAME, 'query').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Assuming there is a button to view details
        self.driver.find_element(By.XPATH, '//a[text()="View Freelancer Details"]').click()
        self.assertIn("Name: John Doe", self.driver.page_source)

    def test_manage_projects(self):
        # Functionalities 7: Test managing projects
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        self.assertIn("Manage Projects", self.driver.title)

    def test_create_new_project(self):
        # Functionalities 8: Test creating a new project
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        
        # Assuming there is a form to create a new project
        self.driver.find_element(By.NAME, 'project_name').send_keys("New Project")
        self.driver.find_element(By.NAME, 'project_description').send_keys("Project Description")
        self.driver.find_element(By.XPATH, '//button[text()="Create Project"]').click()

        self.assertIn("Project created successfully", self.driver.page_source)

    def test_view_project_lists(self):
        # Functionalities 9: Test viewing project lists
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        self.assertIn("Project List", self.driver.page_source)

    def test_profile_management(self):
        # Functionalities 10: Test profile management
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Profile').click()
        self.assertIn("Current Profile Details", self.driver.page_source)

    def test_update_user_profile(self):
        # Functionalities 11: Test updating user profile
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Profile').click()
        
        # Assuming there are fields to update username and email
        self.driver.find_element(By.NAME, 'username').clear()
        self.driver.find_element(By.NAME, 'username').send_keys("updated_user")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()

        self.assertIn("Profile updated successfully", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
