import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestSocialLearnApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8242/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8242/register')  # Navigate to the Registration Page
        self.assertIn("Register", self.driver.title)  # Check if Registration form is displayed

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)  # Check if redirected to Dashboard

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8242/')  # Go back to login page
        self.login("invalid_user", "invalid_pass")
        time.sleep(1)  # Wait for the error message
        self.assertIn("Invalid credentials", self.driver.page_source)  # Check for error message

    def test_profile_management(self):
        # Functionality 3: User Profile Management
        self.login("user1", "user123")  # Login successfully
        self.driver.get('http://localhost:8242/profile')  # Navigate to Profile Page
        self.assertIn("Profile Management", self.driver.title)  # Check if Profile Page is displayed

        # Update profile with new interests
        self.driver.find_element(By.NAME, 'interests').send_keys("Math, Science")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        time.sleep(1)  # Wait for the profile to update
        self.assertIn("Profile updated", self.driver.page_source)  # Check for confirmation message

    def test_study_groups(self):
        # Functionality 4: Join Study Groups
        self.login("user1", "user123")  # Login successfully
        self.driver.get('http://localhost:8242/study_groups')  # Navigate to Study Groups Page
        self.assertIn("Available Study Groups", self.driver.title)  # Check if Study Groups Page is displayed

        # Attempt to join a study group (assuming a join button exists)
        self.driver.find_element(By.XPATH, '//button[text()="Join"]').click()
        time.sleep(1)  # Wait for the join action
        self.assertIn("Successfully joined", self.driver.page_source)  # Check for confirmation message

    def test_resources(self):
        # Functionality 5: Share and Access Educational Resources
        self.login("user1", "user123")  # Login successfully
        self.driver.get('http://localhost:8242/resources')  # Navigate to Resources Page
        self.assertIn("Share Educational Resources", self.driver.title)  # Check if Resources Page is displayed

        # Share a new educational resource
        self.driver.find_element(By.NAME, 'title').send_keys("New Resource")
        self.driver.find_element(By.NAME, 'link').send_keys("https://example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Share Resource"]').click()
        time.sleep(1)  # Wait for the resource to be shared
        self.assertIn("Resource shared", self.driver.page_source)  # Check for confirmation message

    def test_messaging(self):
        # Functionality 6: Messaging in Study Groups
        self.login("user1", "user123")  # Login successfully
        self.driver.get('http://localhost:8242/messaging')  # Navigate to Messaging Page
        self.assertIn("Messaging", self.driver.title)  # Check if Messaging Page is displayed

        # Send a message
        self.driver.find_element(By.NAME, 'sender').send_keys("user1")
        self.driver.find_element(By.NAME, 'content').send_keys("Hello everyone!")
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()
        time.sleep(1)  # Wait for the message to be sent
        self.assertIn("Message sent", self.driver.page_source)  # Check for confirmation message

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("user1", "user123")  # Login successfully
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click the Logout button
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.title)  # Check if redirected to the Login Page

if __name__ == '__main__':
    unittest.main()
