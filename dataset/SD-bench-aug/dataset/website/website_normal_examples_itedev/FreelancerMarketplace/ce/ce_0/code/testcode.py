import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the web application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

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
        self.assertIn("Welcome", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
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
        self.assertIn("Welcome", self.driver.page_source)

    def test_searching_for_freelancers(self):
        # Functionalities 5: Test searching for freelancers
        self.login("admin", "admin123")
        search_query = "John Doe"
        search_box = self.driver.find_element(By.NAME, 'search')
        search_box.send_keys(search_query)
        search_box.submit()
        time.sleep(1)  # Wait for the search results to load
        self.assertIn("John Doe", self.driver.page_source)

    def test_viewing_freelancer_profiles(self):
        # Functionalities 6: Test viewing freelancer profiles
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Freelancer Details').click()
        time.sleep(1)  # Wait for the profile page to load
        self.assertIn("Freelancer Profile", self.driver.title)

    def test_managing_projects(self):
        # Functionalities 7: Test managing projects
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage All Projects').click()
        time.sleep(1)  # Wait for the project management page to load
        self.assertIn("Project Management", self.driver.title)

    def test_creating_new_project(self):
        # Functionalities 8: Test creating a new project
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage All Projects').click()
        time.sleep(1)  # Wait for the project management page to load

        # Fill out the project creation form
        self.driver.find_element(By.NAME, 'project_name').send_keys("New Project")
        self.driver.find_element(By.NAME, 'description').send_keys("Project Description")
        self.driver.find_element(By.NAME, 'freelancer').send_keys("John Doe")
        self.driver.find_element(By.XPATH, '//button[text()="Create Project"]').click()
        time.sleep(1)  # Wait for the project to be created

        # Verify the project creation confirmation
        self.assertIn("Project created successfully!", self.driver.page_source)

    def test_viewing_project_lists(self):
        # Functionalities 9: Test viewing project lists
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage All Projects').click()
        time.sleep(1)  # Wait for the project management page to load
        self.assertIn("Existing Projects", self.driver.page_source)

    def test_profile_management(self):
        # Functionalities 10: Test profile management
        self.login("admin", "admin123")
        # Assuming there's a link to profile management
        self.driver.find_element(By.LINK_TEXT, 'Profile Management').click()
        time.sleep(1)  # Wait for the profile management page to load
        self.assertIn("Profile Management", self.driver.title)

    def test_updating_user_profile(self):
        # Functionalities 11: Test updating user profile
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile Management').click()
        time.sleep(1)  # Wait for the profile management page to load

        # Update profile details
        self.driver.find_element(By.NAME, 'username').clear()
        self.driver.find_element(By.NAME, 'username').send_keys("updated_user")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the update to process

        # Verify the profile update confirmation
        self.assertIn("Profile updated successfully!", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
