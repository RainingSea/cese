import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestSocialLearnApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8243/')  # Use the port from main.py

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:8243/')  # Navigate to login page
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8243/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8243/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.login("admin", "wrong_password")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_profile_management(self):
        # Functionality 3: User Profile Management
        self.login("user1", "user123")  # Login to access profile
        self.driver.get('http://localhost:8243/profile')
        self.assertIn("Profile Management", self.driver.title)

        # Update profile interests
        self.driver.find_element(By.NAME, 'interests').send_keys("Math, Science")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        self.assertIn("Profile updated successfully", self.driver.page_source)

        # Attempt to update with empty interests
        self.driver.find_element(By.NAME, 'interests').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        self.assertIn("All fields are required", self.driver.page_source)

    def test_join_study_groups(self):
        # Functionality 4: Join Study Groups
        self.login("user1", "user123")  # Login to access groups
        self.driver.get('http://localhost:8243/groups')
        self.assertIn("Study Groups", self.driver.title)

        # Join a group
        self.driver.find_element(By.NAME, 'group_name').send_keys("Math Study Group")
        self.driver.find_element(By.XPATH, '//button[text()="Join Group"]').click()
        self.assertIn("Successfully joined the group", self.driver.page_source)

        # Attempt to join a full group (not implemented in the codebase)
        self.fail("Joining a full group is not implemented")

    def test_share_resources(self):
        # Functionality 5: Share and Access Educational Resources
        self.login("user1", "user123")  # Login to access resources
        self.driver.get('http://localhost:8243/resources')
        self.assertIn("Resource Sharing", self.driver.title)

        # Share a resource
        self.driver.find_element(By.NAME, 'resource').send_keys("New Resource")
        self.driver.find_element(By.XPATH, '//button[text()="Share Resource"]').click()
        self.assertIn("Resource shared successfully", self.driver.page_source)

        # Attempt to share an invalid resource (not implemented in the codebase)
        self.fail("Sharing an invalid resource is not implemented")

    def test_send_message(self):
        # Functionality 6: Messaging in Study Groups
        self.login("user1", "user123")  # Login to access messages
        self.driver.get('http://localhost:8243/messages')
        self.assertIn("Messaging", self.driver.title)

        # Send a message
        self.driver.find_element(By.NAME, 'to_user').send_keys("admin")
        self.driver.find_element(By.NAME, 'message').send_keys("Hello!")
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()
        self.assertIn("Message sent successfully", self.driver.page_source)

        # Attempt to send an empty message
        self.driver.find_element(By.NAME, 'message').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()
        self.assertIn("Message cannot be empty", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Login to logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the Dashboard
        self.driver.get('http://localhost:8243/')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 8: Navigate Back to Dashboard
        self.login("user1", "user123")  # Login to navigate
        self.driver.get('http://localhost:8243/profile')
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        self.assertIn("Dashboard", self.driver.title)

    def test_view_resource_details(self):
        # Functionality 9: View Educational Resource Details
        self.login("user1", "user123")  # Login to view resources
        self.driver.get('http://localhost:8243/resources')
        self.assertIn("Resource Sharing", self.driver.title)

        # Click on a resource to view details (not implemented in the codebase)
        self.fail("Viewing resource details is not implemented")

if __name__ == '__main__':
    unittest.main()
