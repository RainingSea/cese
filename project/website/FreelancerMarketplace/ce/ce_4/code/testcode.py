import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Allow some time for the server to start

        # Initialize the webdriver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8948/')

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
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

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
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
        self.assertIn("Welcome to the Freelancer Platform", self.driver.page_source)

    def test_search_freelancers(self):
        # Functionalities 5: Test searching for freelancers
        self.login("admin", "admin123")

        # Enter a freelancer name in the search field and submit
        self.driver.find_element(By.NAME, 'name').send_keys("Freelancer A")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        # Verify that the search results display the freelancer
        self.assertIn("Freelancer A", self.driver.page_source)

    def test_view_freelancer_profiles(self):
        # Functionalities 6: Test viewing freelancer profiles
        self.fail("Not implemented")

    def test_manage_projects(self):
        # Functionalities 7: Test managing projects
        self.login("admin", "admin123")

        # Navigate to Project Management Page
        self.driver.find_element(By.LINK_TEXT, 'Go to Project Management').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Project Management Page has loaded
        self.assertIn("Manage Projects", self.driver.page_source)

    def test_create_new_project(self):
        # Functionalities 8: Test creating a new project
        self.login("admin", "admin123")

        # Navigate to Project Management Page
        self.driver.find_element(By.LINK_TEXT, 'Go to Project Management').click()
        time.sleep(1)  # Wait for the next page to load

        # Enter project details and submit
        self.driver.find_element(By.NAME, 'name').send_keys("Project C")
        self.driver.find_element(By.NAME, 'description').send_keys("Description of Project C")
        self.driver.find_element(By.NAME, 'freelancer').send_keys("Freelancer A")
        self.driver.find_element(By.XPATH, '//button[text()="Create Project"]').click()
        time.sleep(1)  # Wait for the project to be created

        # Verify that the user is redirected to the home page
        self.assertIn("Welcome to the Freelancer Platform", self.driver.page_source)

    def test_view_project_lists(self):
        # Functionalities 9: Test viewing project lists
        self.fail("Not implemented")

    def test_profile_management(self):
        # Functionalities 10: Test profile management
        self.login("admin", "admin123")

        # Navigate to Profile Management Page
        self.driver.find_element(By.LINK_TEXT, 'Go to Profile Management').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Profile Management Page has loaded
        self.assertIn("Manage Profile", self.driver.page_source)

    def test_update_user_profile(self):
        # Functionalities 11: Test updating the user profile
        self.login("admin", "admin123")

        # Navigate to Profile Management Page
        self.driver.find_element(By.LINK_TEXT, 'Go to Profile Management').click()
        time.sleep(1)  # Wait for the next page to load

        # Update email and submit
        self.driver.find_element(By.NAME, 'email').clear()
        self.driver.find_element(By.NAME, 'email').send_keys("updated_admin@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the profile to be updated

        # Verify that the user is redirected to the home page
        self.assertIn("Welcome to the Freelancer Platform", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
