import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestFreelancerMarketplace(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8384/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        
        # Verify that the home page has loaded
        self.assertIn("Welcome to Freelancer Marketplace", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        
        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_access_home_after_login(self):
        # Functionalities 4: Test accessing home page after login
        self.login("admin", "admin123")
        
        # Verify that the home page shows the welcome message
        self.assertIn("Welcome to Freelancer Marketplace", self.driver.page_source)

    def test_view_projects(self):
        # Functionalities 9: Test viewing project lists
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Projects').click()
        
        # Verify that the projects page has loaded
        self.assertIn("Projects", self.driver.title)

    def test_profile_management(self):
        # Functionalities 10: Test navigating to profile management page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile Management').click()
        
        # Verify that the profile management page has loaded
        self.assertIn("Profile Management", self.driver.title)

    def test_update_profile(self):
        # Functionalities 11: Test updating the user profile
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile Management').click()

        # Update username and email
        self.driver.find_element(By.NAME, 'username').clear()
        self.driver.find_element(By.NAME, 'username').send_keys("updated_user")
        self.driver.find_element(By.NAME, 'email').send_keys("updated_email@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Update"]').click()

        # Verify that the profile is updated
        self.assertIn("Profile Management", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
