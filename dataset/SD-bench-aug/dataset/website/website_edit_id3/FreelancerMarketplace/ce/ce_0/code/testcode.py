import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8129')

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
        # Functionalities 1: User Login
        self.login("admin", "adminpass")
        self.assertIn("Welcome, admin", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Login", self.driver.title)

    def test_access_home_page_after_login(self):
        # Functionalities 4: Accessing Home Page after Login
        self.login("admin", "adminpass")
        self.assertIn("Welcome, admin", self.driver.page_source)

    def test_search_freelancers(self):
        # Functionalities 5: Searching for Freelancers
        self.login("admin", "adminpass")
        self.driver.find_element(By.NAME, 'search_name').send_keys("user1")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load
        self.assertIn("user1", self.driver.page_source)

    def test_view_freelancer_profiles(self):
        # Functionalities 6: Viewing Freelancer Profiles
        self.fail("Not implemented")

    def test_manage_projects(self):
        # Functionalities 7: Managing Projects
        self.fail("Not implemented")

    def test_create_new_project(self):
        # Functionalities 8: Creating a New Project
        self.fail("Not implemented")

    def test_view_project_lists(self):
        # Functionalities 9: Viewing Project Lists
        self.fail("Not implemented")

    def test_profile_management(self):
        # Functionalities 10: Profile Management
        self.fail("Not implemented")

    def test_update_user_profile(self):
        # Functionalities 11: Updating the User Profile
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
