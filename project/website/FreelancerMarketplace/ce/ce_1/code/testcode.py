import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8383/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Welcome to Freelancer Marketplace", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.assertIn("Login", self.driver.title)

    def test_access_home_page_after_login(self):
        # Functionalities 4: Accessing Home Page after Login
        self.login("admin", "admin123")
        self.assertIn("Welcome to Freelancer Marketplace", self.driver.page_source)

    def test_searching_for_freelancers(self):
        # Functionalities 5: Searching for Freelancers
        self.login("admin", "admin123")
        search_input = self.driver.find_element(By.NAME, 'search')
        search_input.send_keys("Alice")
        search_input.submit()
        self.assertIn("Alice", self.driver.page_source)

    def test_viewing_freelancer_profiles(self):
        # Functionalities 6: Viewing Freelancer Profiles
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Alice").click()
        self.assertIn("Expert in web development", self.driver.page_source)

    def test_managing_projects(self):
        # Functionalities 7: Managing Projects
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Manage Projects").click()
        self.assertIn("Manage Projects", self.driver.title)

    def test_creating_new_project(self):
        # Functionalities 8: Creating a New Project
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Manage Projects").click()
        self.driver.find_element(By.NAME, 'project_name').send_keys("New Project")
        self.driver.find_element(By.NAME, 'description').send_keys("Project Description")
        self.driver.find_element(By.NAME, 'freelancer').send_keys("Alice")
        self.driver.find_element(By.XPATH, '//button[text()="Create Project"]').click()
        self.assertIn("New Project", self.driver.page_source)

    def test_viewing_project_lists(self):
        # Functionalities 9: Viewing Project Lists
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Manage Projects").click()
        self.assertIn("Website Redesign", self.driver.page_source)

    def test_profile_management(self):
        # Functionalities 10: Profile Management
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Profile Management").click()
        self.assertIn("Profile Management", self.driver.title)

    def test_updating_user_profile(self):
        # Functionalities 11: Updating the User Profile
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Profile Management").click()
        self.driver.find_element(By.NAME, 'username').send_keys("updated_user")
        self.driver.find_element(By.NAME, 'email').send_keys("updated_email@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        self.assertIn("Profile Management", self.driver.title)

if __name__ == '__main__':
    unittest.main()
