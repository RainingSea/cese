import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestSocialLearnApp(unittest.TestCase):

    def setUp(self):
        # Start the server and initialize the webdriver
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8080/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the server process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.get('http://localhost:8080/register')  # Assuming the registration page URL
        self.assertIn("Register", self.driver.title)

        # Enter valid username and password
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify registration success
        self.assertIn("Registration successful", self.driver.page_source)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8080/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8080/')
        self.assertIn("Login", self.driver.title)

        # Enter valid username and password
        self.login("admin", "admin123")

        # Verify successful login
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8080/')
        self.login("admin", "wrongpassword")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_user_profile_management(self):
        # Login successfully
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8080/profile')  # Assuming the profile page URL
        self.assertIn("Profile", self.driver.title)

        # Update profile
        self.driver.find_element(By.NAME, 'interests').clear()
        self.driver.find_element(By.NAME, 'interests').send_keys("New Interests")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()

        # Verify profile update success
        self.assertIn("Profile updated successfully", self.driver.page_source)

        # Attempt to update profile with invalid data
        self.driver.find_element(By.NAME, 'interests').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        self.assertIn("All fields are required", self.driver.page_source)

    def test_join_study_groups(self):
        # Login successfully
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8080/study_groups')  # Assuming the study groups page URL
        self.assertIn("Study Groups", self.driver.title)

        # Join a study group
        self.driver.find_element(By.XPATH, '//button[text()="Join Math Study Group"]').click()
        self.assertIn("Successfully joined the group", self.driver.page_source)

        # Attempt to join a full study group (not implemented, assuming a failure case)
        self.driver.find_element(By.XPATH, '//button[text()="Join Full Group"]').click()
        self.assertIn("Study group is full", self.driver.page_source)

    def test_share_and_access_resources(self):
        # Login successfully
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8080/resources')  # Assuming the resources page URL
        self.assertIn("Resources", self.driver.title)

        # Share a new resource
        self.driver.find_element(By.NAME, 'resource').send_keys("New Resource")
        self.driver.find_element(By.XPATH, '//button[text()="Share"]').click()
        self.assertIn("Resource shared successfully", self.driver.page_source)

        # Attempt to upload an invalid resource (not implemented, assuming a failure case)
        self.driver.find_element(By.NAME, 'resource').send_keys("Invalid Resource Format")
        self.driver.find_element(By.XPATH, '//button[text()="Share"]').click()
        self.assertIn("Invalid file format", self.driver.page_source)

    def test_messaging_in_study_groups(self):
        # Login successfully
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8080/study_group_chat')  # Assuming the chat page URL
        self.assertIn("Study Group Chat", self.driver.title)

        # Send a message
        self.driver.find_element(By.NAME, 'message').send_keys("Hello everyone!")
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()
        self.assertIn("Message sent successfully", self.driver.page_source)

        # Attempt to send an empty message
        self.driver.find_element(By.NAME, 'message').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()
        self.assertIn("Message cannot be empty", self.driver.page_source)

    def test_user_logout(self):
        # Login successfully
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8080/dashboard')  # Assuming the dashboard page URL

        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the Dashboard
        self.driver.get('http://localhost:8080/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Login successfully
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8080/profile')  # Assuming the profile page URL
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        self.assertIn("Dashboard", self.driver.title)

    def test_view_educational_resource_details(self):
        # Login successfully
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8080/resources')  # Assuming the resources page URL
        self.driver.find_element(By.LINK_TEXT, 'View Resource').click()  # Assuming a resource link
        self.assertIn("Resource Details", self.driver.title)

        # Attempt to view details of a deleted resource (not implemented, assuming a failure case)
        self.driver.get('http://localhost:8080/resources/deleted_resource')  # Assuming a deleted resource URL
        self.assertIn("Resource not available", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
