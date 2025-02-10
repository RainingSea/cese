import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8538/login') 

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
        self.assertIn("Welcome to Freelancer Marketplace", self.driver.page_source)

    def test_searching_for_freelancers(self):
        # Functionalities 5: Test searching for freelancers
        self.login("admin", "admin123")

        # Enter a search term and submit
        self.driver.find_element(By.NAME, 'search').send_keys("user1")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for search results

        # Verify search results
        self.assertIn("user1", self.driver.page_source)

    def test_viewing_freelancer_profiles(self):
        # Functionalities 6: Test viewing freelancer profiles
        self.fail("not implemented")

    def test_managing_projects(self):
        # Functionalities 7: Test managing projects
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Manage Projects Page has loaded
        self.assertIn("Manage Projects", self.driver.title)

    def test_creating_a_new_project(self):
        # Functionalities 8: Test creating a new project
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load

        # Enter project details
        self.driver.find_element(By.NAME, 'name').send_keys("Project Gamma")
        self.driver.find_element(By.NAME, 'description').send_keys("Description for Project Gamma")
        self.driver.find_element(By.NAME, 'assigned_freelancer').send_keys("user1")
        self.driver.find_element(By.XPATH, '//button[text()="Create Project"]').click()
        time.sleep(1)  # Wait for the project to be created

        # Verify the project is listed
        self.assertIn("Project Gamma", self.driver.page_source)

    def test_viewing_project_lists(self):
        # Functionalities 9: Test viewing project lists
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify project list is displayed
        self.assertIn("Existing Projects", self.driver.page_source)

    def test_profile_management(self):
        # Functionalities 10: Test profile management
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile Management').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify profile management page is displayed
        self.assertIn("Profile Management", self.driver.title)

    def test_updating_user_profile(self):
        # Functionalities 11: Test updating the user profile
        self.fail("not implemented")

if __name__ == '__main__':
    unittest.main()
