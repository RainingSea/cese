import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8539/')  # Open the login page

    def tearDown(self):
        # Close the web driver session and stop the server
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
        self.assertIn("Welcome", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
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

    def test_access_home_after_login(self):
        # Functionalities 4: Test accessing home page after login
        self.login("admin", "admin123")
        self.assertIn("Welcome", self.driver.page_source)

    def test_search_freelancers(self):
        # Functionalities 5: Test searching for freelancers
        self.login("admin", "admin123")
        self.fail("Search functionality not implemented")

    def test_view_freelancer_profiles(self):
        # Functionalities 6: Test viewing freelancer profiles
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'John Doe').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("John Doe", self.driver.page_source)

    def test_manage_projects(self):
        # Functionalities 7: Test managing projects
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Manage Projects", self.driver.title)

    def test_create_new_project(self):
        # Functionalities 8: Test creating a new project
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load

        self.driver.find_element(By.NAME, 'name').send_keys("Project C")
        self.driver.find_element(By.NAME, 'description').send_keys("Description of Project C")
        self.driver.find_element(By.NAME, 'freelancer_assigned').send_keys("John Doe")
        self.driver.find_element(By.XPATH, '//button[text()="Create Project"]').click()
        time.sleep(1)  # Wait for the project to be created

        self.assertIn("Project C", self.driver.page_source)

    def test_view_project_lists(self):
        # Functionalities 9: Test viewing project lists
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Project A", self.driver.page_source)

    def test_profile_management(self):
        # Functionalities 10: Test profile management
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Profile').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Profile Management", self.driver.title)

    def test_update_user_profile(self):
        # Functionalities 11: Test updating the user profile
        self.fail("Profile update functionality not implemented")

if __name__ == '__main__':
    unittest.main()
