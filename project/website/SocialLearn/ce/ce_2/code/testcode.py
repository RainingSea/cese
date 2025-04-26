import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestSocialLearnApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8244/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()

        # Verify that the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Expectation: An error message is displayed
        self.assertIn("already taken", self.driver.page_source)

    def test_user_login(self):
        # Test valid login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Test invalid login
        self.driver.get('http://localhost:8244/')  # Go back to login page
        self.login("admin", "wrong_password")
        self.assertIn("incorrect", self.driver.page_source)

    def test_profile_management(self):
        # Login successfully
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8244/profile')

        # Verify current profile information is displayed
        self.assertIn("Profile Management", self.driver.title)

        # Update profile with new interests
        interests = "Math, Science"
        self.driver.find_element(By.NAME, 'interests').send_keys(interests)
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()

        # Expectation: Profile updated successfully
        self.assertIn("Profile updated", self.driver.page_source)

        # Attempt to update with invalid data (empty fields)
        self.driver.find_element(By.NAME, 'interests').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        self.assertIn("required", self.driver.page_source)

    def test_join_study_groups(self):
        # Login successfully
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8244/study_groups')

        # Expectation: A list of available study groups is displayed
        self.assertIn("Study Groups", self.driver.title)

        # Attempt to join a group (assuming the join button exists)
        self.driver.find_element(By.XPATH, '//button[text()="Join Math Study Group"]').click()
        self.assertIn("joined successfully", self.driver.page_source)

        # Attempt to join a full group (not implemented, so we fail)
        self.fail("Test for joining a full group not implemented")

    def test_share_access_resources(self):
        # Login successfully
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8244/resources')

        # Expectation: A list of shared educational resources is displayed
        self.assertIn("Shared Resources", self.driver.title)

        # Attempt to upload a new educational resource (not implemented, so we fail)
        self.fail("Test for sharing resources not implemented")

    def test_messaging_in_study_groups(self):
        # Login successfully
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8244/messages')

        # Expectation: The study group chat interface is displayed
        self.assertIn("Messages", self.driver.title)

        # Attempt to send a message (not implemented, so we fail)
        self.fail("Test for sending messages not implemented")

    def test_user_logout(self):
        # Login successfully
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the Dashboard Page after logging out
        self.driver.get('http://localhost:8244/profile')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Login successfully
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8244/profile')

        # Click the "Back to Dashboard" button (assuming it exists)
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        self.assertIn("Dashboard", self.driver.title)

    def test_view_resource_details(self):
        # Login successfully
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8244/resources')

        # Click on a specific educational resource (assuming it exists)
        self.driver.find_element(By.LINK_TEXT, 'Python for Beginners').click()
        self.assertIn("Python for Beginners", self.driver.page_source)

        # Attempt to view details of a deleted resource (not implemented, so we fail)
        self.fail("Test for viewing deleted resource details not implemented")

if __name__ == '__main__':
    unittest.main()
