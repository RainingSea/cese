import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Allow time for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8457/') 

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

        # Verify that the Home Page has loaded
        self.assertIn("Welcome to the Freelancer Platform", self.driver.page_source)

    def test_navigate_to_registration_page(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
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

        # Verify that the Home Page has loaded
        self.assertIn("Welcome to the Freelancer Platform", self.driver.page_source)

    def test_searching_for_freelancers(self):
        # Functionalities 5: Test searching for freelancers
        self.login("admin", "admin123")

        # Since there's no search functionality implemented, this test will fail
        self.fail("Search functionality not implemented")

    def test_viewing_freelancer_profiles(self):
        # Functionalities 6: Test viewing freelancer profiles
        self.login("admin", "admin123")

        # Since there's no view profile functionality implemented, this test will fail
        self.fail("View freelancer profile functionality not implemented")

    def test_managing_projects(self):
        # Functionalities 7: Test managing projects
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Project Management Page has loaded
        self.assertIn("Project Management", self.driver.title)

    def test_creating_a_new_project(self):
        # Functionalities 8: Test creating a new project
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load

        project_name = "New Project"
        project_description = "Project Description"
        freelancer_name = "John Doe"

        # Fill out the new project form
        self.driver.find_element(By.NAME, 'name').send_keys(project_name)
        self.driver.find_element(By.NAME, 'description').send_keys(project_description)
        self.driver.find_element(By.NAME, 'freelancer').send_keys(freelancer_name)
        self.driver.find_element(By.XPATH, '//button[text()="Create Project"]').click()
        time.sleep(1)  # Wait for the project to be created

        # Verify that the new project is displayed on the Project Management Page
        self.assertIn(project_name, self.driver.page_source)

    def test_viewing_project_lists(self):
        # Functionalities 9: Test viewing project lists
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Project Management Page shows projects
        projects = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(projects), 0, "No projects found.")

    def test_profile_management(self):
        # Functionalities 10: Test profile management
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Profile').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Profile Management Page has loaded
        self.assertIn("Profile Management", self.driver.title)

    def test_updating_the_user_profile(self):
        # Functionalities 11: Test updating the user profile
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Profile').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "updated_user"
        new_email = "updated_email@example.com"

        # Fill out the profile update form
        self.driver.find_element(By.NAME, 'new_username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'new_email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the profile to be updated

        # Since there's no confirmation message implemented, this test will fail
        self.fail("Profile update confirmation not implemented")

if __name__ == '__main__':
    unittest.main()
