import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8306')

    def tearDown(self):
        # Close the web driver session and stop the web application
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
        self.assertIn("Home", self.driver.title)

    def test_navigate_to_registration(self):
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
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_access_home_page_after_login(self):
        # Functionalities 4: Test accessing home page after login
        self.login("admin", "admin123")

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_search_freelancers(self):
        # Functionalities 5: Test searching for freelancers
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Search Freelancers').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Freelancers Page has loaded
        self.assertIn("Freelancers", self.driver.title)

    def test_view_freelancer_profiles(self):
        # Functionalities 6: Test viewing freelancer profiles
        self.fail("not implemented")

    def test_manage_projects(self):
        # Functionalities 7: Test managing projects
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Manage Projects Page has loaded
        self.assertIn("Manage Projects", self.driver.title)

    def test_create_new_project(self):
        # Functionalities 8: Test creating a new project
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load

        project_name = "New Project"
        project_description = "Description of New Project"
        freelancer_name = "Freelancer A"

        # Fill out the new project form
        self.driver.find_element(By.NAME, 'project_name').send_keys(project_name)
        self.driver.find_element(By.NAME, 'project_description').send_keys(project_description)
        self.driver.find_element(By.NAME, 'freelancer_name').send_keys(freelancer_name)
        self.driver.find_element(By.XPATH, '//button[text()="Create Project"]').click()
        time.sleep(1)  # Wait for saving the project

        # Verify that the new project is displayed on the Manage Projects Page
        self.assertIn(project_name, self.driver.page_source)

    def test_view_project_lists(self):
        # Functionalities 9: Test viewing project lists
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the project list is displayed
        projects = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(projects), 0, "No projects found.")

    def test_profile_management(self):
        # Functionalities 10: Test profile management
        self.fail("not implemented")

    def test_update_user_profile(self):
        # Functionalities 11: Test updating the user profile
        self.fail("not implemented")

if __name__ == '__main__':
    unittest.main()
