import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestFreelancerMarketplaceApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8169/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Welcome to the Home Page", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        new_username = "new_user"
        new_password = "new_password"
        
        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_access_home_page_after_login(self):
        # Functionalities 4: Test accessing home page after login
        self.login("admin", "admin123")
        self.assertIn("Welcome to the Home Page", self.driver.page_source)

    def test_search_freelancers(self):
        # Functionalities 5: Test searching for freelancers
        self.login("admin", "admin123")
        search_input = self.driver.find_element(By.XPATH, '//input[@placeholder="Search for freelancers..."]')
        search_input.send_keys("John Doe")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that search results display freelancers matching the entered name
        self.assertIn("John Doe", self.driver.page_source)

    def test_view_freelancer_profiles(self):
        # Functionalities 6: Test viewing freelancer profiles
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//input[@placeholder="Search for freelancers..."]').send_keys("John Doe")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        # Assuming there is a button to view freelancer details
        self.driver.find_element(By.LINK_TEXT, 'View Freelancer Details').click()
        self.assertIn("Freelancer Profile", self.driver.title)

    def test_manage_projects(self):
        # Functionalities 7: Test managing projects
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        self.assertIn("Manage Projects", self.driver.title)

    def test_create_new_project(self):
        # Functionalities 8: Test creating a new project
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        
        project_name = "New Project"
        project_description = "Description of new project"
        freelancer_id = 0  # Assuming freelancer ID is 0 for testing

        self.driver.find_element(By.NAME, 'name').send_keys(project_name)
        self.driver.find_element(By.NAME, 'description').send_keys(project_description)
        self.driver.find_element(By.NAME, 'freelancer_id').send_keys(freelancer_id)
        self.driver.find_element(By.XPATH, '//button[text()="Create Project"]').click()

        # Verify that the project is created successfully
        self.assertIn(project_name, self.driver.page_source)

    def test_view_project_lists(self):
        # Functionalities 9: Test viewing project lists
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
        self.assertIn("Existing Projects", self.driver.page_source)

    def test_profile_management(self):
        # Functionalities 10: Test profile management
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Profile').click()
        self.assertIn("Manage Profile", self.driver.title)

    def test_update_user_profile(self):
        # Functionalities 11: Test updating the user profile
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Profile').click()
        
        new_username = "updated_user"
        new_email = "updated_email@example.com"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()

        # Verify that the profile is updated successfully
        self.assertIn("Profile updated successfully", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
