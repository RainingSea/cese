import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import subprocess
import time

class TestSocialLearnApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8635/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("already taken", self.driver.page_source)

    def test_user_login(self):
        # Verify the Login form is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and the user is redirected
        self.assertNotIn("Login", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8635/')  # Navigate back to login
        self.login("invalid_user", "wrong_password")

        # Verify an error message is displayed
        self.assertIn("incorrect", self.driver.page_source)

    def test_user_profile_management(self):
        # Login successfully and navigate to the Profile Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8635/profile')
        time.sleep(1)  # Wait for the next page to load

        # Verify the user's current profile information is displayed
        self.assertIn("Profile of admin", self.driver.page_source)

        # Update the profile with new areas of interest and save changes
        self.driver.find_element(By.NAME, 'interests').clear()
        self.driver.find_element(By.NAME, 'interests').send_keys("math,science,technology")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the profile is updated successfully
        self.assertIn("Profile of admin", self.driver.page_source)

        # Attempt to update the profile with invalid data
        self.driver.find_element(By.NAME, 'interests').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("all fields are required", self.driver.page_source)

    def test_join_study_groups(self):
        # Login successfully and navigate to the Study Groups Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8635/study_groups')
        time.sleep(1)  # Wait for the next page to load

        # Verify a list of available study groups is displayed
        self.assertIn("Study Groups", self.driver.page_source)

        # Select a study group and click the "Join" button
        # Note: The join functionality is not implemented in the codebase
        self.fail("Join study group functionality not implemented")

    def test_share_and_access_educational_resources(self):
        # Login successfully and navigate to the Resources Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8635/resources')
        time.sleep(1)  # Wait for the next page to load

        # Verify a list of shared educational resources is displayed
        self.assertIn("Resources", self.driver.page_source)

        # Upload a new educational resource
        self.driver.find_element(By.NAME, 'title').send_keys("New Resource")
        self.driver.find_element(By.NAME, 'link').send_keys("https://example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Share Resource"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the resource is uploaded successfully
        self.assertIn("New Resource", self.driver.page_source)

        # Attempt to upload a resource with invalid format
        # Note: The invalid format check is not implemented in the codebase
        self.fail("Invalid format check not implemented")

    def test_messaging_in_study_groups(self):
        # Login successfully and navigate to a study group
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8635/messages')
        time.sleep(1)  # Wait for the next page to load

        # Verify the study group chat interface is displayed
        self.assertIn("Messages", self.driver.page_source)

        # Send a message in the study group chat
        self.driver.find_element(By.NAME, 'receiver').send_keys("user1")
        self.driver.find_element(By.NAME, 'content').send_keys("Hello!")
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the message is sent successfully
        self.assertIn("Hello!", self.driver.page_source)

        # Attempt to send an empty message
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("message cannot be empty", self.driver.page_source)

    def test_user_logout(self):
        # Login successfully
        self.login("admin", "admin123")

        # Click the Logout button
        # Note: The logout functionality is not implemented in the codebase
        self.fail("Logout functionality not implemented")

    def test_navigate_back_to_dashboard(self):
        # Login successfully and navigate to the Profile Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8635/profile')
        time.sleep(1)  # Wait for the next page to load

        # Click the "Back to Dashboard" button
        # Note: The back to dashboard functionality is not implemented in the codebase
        self.fail("Back to dashboard functionality not implemented")

    def test_view_educational_resource_details(self):
        # Login successfully and navigate to the Resources Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8635/resources')
        time.sleep(1)  # Wait for the next page to load

        # Click on a specific educational resource to view details
        # Note: The view details functionality is not implemented in the codebase
        self.fail("View educational resource details functionality not implemented")

if __name__ == '__main__':
    unittest.main()
