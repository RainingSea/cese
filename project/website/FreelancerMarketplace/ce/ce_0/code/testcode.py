import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the actual port from main.py

    def tearDown(self):
        # Close the web driver session and the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Welcome to the Home Page", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.assertIn("Registration", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.driver.find_element(By.ID, 'username').send_keys("new_user")
        self.driver.find_element(By.ID, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        self.assertIn("Login", self.driver.title)

    def test_access_home_page_after_login(self):
        # Functionalities 4: Accessing Home Page after Login
        self.login("admin", "admin123")
        self.assertIn("Welcome to the Home Page", self.driver.page_source)

    def test_searching_for_freelancers(self):
        # Functionalities 5: Searching for Freelancers
        self.login("admin", "admin123")
        search_box = self.driver.find_element(By.ID, 'freelancer_name')
        search_box.send_keys("John Doe")
        self.driver.find_element(By.XPATH, '//input[@value="Search"]').click()
        self.assertIn("John Doe", self.driver.page_source)

    def test_viewing_freelancer_profiles(self):
        # Functionalities 6: Viewing Freelancer Profiles
        self.login("admin", "admin123")
        search_box = self.driver.find_element(By.ID, 'freelancer_name')
        search_box.send_keys("John Doe")
        self.driver.find_element(By.XPATH, '//input[@value="Search"]').click()
        self.driver.find_element(By.LINK_TEXT, 'View Freelancer Details').click()
        self.assertIn("Freelancer Profile", self.driver.title)

    def test_managing_projects(self):
        # Functionalities 7: Managing Projects
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Manage All Projects"]').click()
        self.assertIn("Project Management", self.driver.title)

    def test_creating_new_project(self):
        # Functionalities 8: Creating a New Project
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Create New Project"]').click()
        self.driver.find_element(By.NAME, 'project_name').send_keys("New Project")
        self.driver.find_element(By.NAME, 'description').send_keys("Project Description")
        self.driver.find_element(By.NAME, 'freelancer').send_keys("John Doe")
        self.driver.find_element(By.XPATH, '//input[@value="Create Project"]').click()
        self.assertIn("Project created successfully", self.driver.page_source)

    def test_viewing_project_lists(self):
        # Functionalities 9: Viewing Project Lists
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Manage All Projects"]').click()
        self.assertIn("Project Alpha", self.driver.page_source)

    def test_profile_management(self):
        # Functionalities 10: Profile Management
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Edit Profile"]').click()
        self.assertIn("Profile Management", self.driver.title)

    def test_updating_user_profile(self):
        # Functionalities 11: Updating the User Profile
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Edit Profile"]').click()
        self.driver.find_element(By.ID, 'username').clear()
        self.driver.find_element(By.ID, 'username').send_keys("updated_user")
        self.driver.find_element(By.ID, 'email').send_keys("updated_email@example.com")
        self.driver.find_element(By.XPATH, '//input[@value="Update Profile"]').click()
        self.assertIn("Profile updated successfully", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
