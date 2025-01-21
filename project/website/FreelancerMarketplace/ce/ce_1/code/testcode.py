import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Allow some time for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8945/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the server process
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
        self.assertIn("Home", self.driver.title)

    def test_searching_for_freelancers(self):
        # Functionalities 5: Test searching for freelancers
        self.login("admin", "admin123")

        # Assuming there's a search field and button (not implemented in the codebase)
        self.fail("Search functionality not implemented")

    def test_viewing_freelancer_profiles(self):
        # Functionalities 6: Test viewing freelancer profiles
        self.login("admin", "admin123")

        # Click on a freelancer link
        self.driver.find_element(By.LINK_TEXT, 'John Doe').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Freelancer Profile Page has loaded
        self.assertIn("John Doe Profile", self.driver.title)

    def test_managing_projects(self):
        # Functionalities 7: Test managing projects
        self.login("admin", "admin123")

        # Click on the "Manage Projects" link
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Project Management Page has loaded
        self.assertIn("Project Management", self.driver.title)

    def test_creating_a_new_project(self):
        # Functionalities 8: Test creating a new project
        self.login("admin", "admin123")

        # Navigate to Project Management Page
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the new project form
        self.driver.find_element(By.NAME, 'name').send_keys("New Project")
        self.driver.find_element(By.NAME, 'description').send_keys("Project Description")
        self.driver.find_element(By.NAME, 'freelancer').send_keys("John Doe")
        self.driver.find_element(By.XPATH, '//button[text()="Create Project"]').click()
        time.sleep(1)  # Wait for the project to be created

        # Verify that the user is redirected to the Home Page
        self.assertIn("Home", self.driver.title)

    def test_viewing_project_lists(self):
        # Functionalities 9: Test viewing project lists
        self.login("admin", "admin123")

        # Navigate to Project Management Page
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Project Management Page has loaded
        self.assertIn("Project Management", self.driver.title)

    def test_profile_management(self):
        # Functionalities 10: Test profile management
        self.login("admin", "admin123")

        # Navigate to Profile Management Page
        self.driver.find_element(By.LINK_TEXT, 'Manage Profile').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Profile Management Page has loaded
        self.assertIn("Profile Management", self.driver.title)

    def test_updating_user_profile(self):
        # Functionalities 11: Test updating the user profile
        self.login("admin", "admin123")

        # Navigate to Profile Management Page
        self.driver.find_element(By.LINK_TEXT, 'Manage Profile').click()
        time.sleep(1)  # Wait for the next page to load

        # Update profile details
        self.driver.find_element(By.NAME, 'username').clear()
        self.driver.find_element(By.NAME, 'username').send_keys("updated_admin")
        self.driver.find_element(By.NAME, 'email').clear()
        self.driver.find_element(By.NAME, 'email').send_keys("admin@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the profile to be updated

        # Verify that the user is redirected to the Home Page
        self.assertIn("Home", self.driver.title)

if __name__ == '__main__':
    unittest.main()
