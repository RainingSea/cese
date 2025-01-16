import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestSocialLearnApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8553')

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

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message is displayed
        self.assertIn("already exists", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8553')
        time.sleep(1)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Dashboard Page
        self.assertNotIn("Login", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8553')
        self.login("invalid_user", "invalid_pass")

        # Verify error message is displayed
        self.assertIn("Login failed", self.driver.page_source)

    def test_user_profile_management(self):
        # Login successfully and navigate to the Profile Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8553/profile')
        time.sleep(1)

        # Update the profile with new areas of interest and save changes
        self.driver.find_element(By.NAME, 'interests').clear()
        self.driver.find_element(By.NAME, 'interests').send_keys("math,science,technology")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)

        # Verify the profile is updated successfully
        self.assertIn("Profile updated", self.driver.page_source)

        # Attempt to update the profile with invalid data
        self.driver.find_element(By.NAME, 'interests').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)

        # Verify error message is displayed
        self.assertIn("all fields are required", self.driver.page_source)

    def test_join_study_groups(self):
        # Login successfully and navigate to the Study Groups Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8553/groups')
        time.sleep(1)

        # Verify a list of available study groups is displayed
        groups = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(groups), 0, "No study groups found.")

        # Select a study group and click the "Join" button
        # Note: The current implementation does not support joining groups via UI, so this will fail
        self.fail("Join study group functionality not implemented")

    def test_share_and_access_educational_resources(self):
        # Login successfully and navigate to the Resources Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8553/resources')
        time.sleep(1)

        # Verify a list of shared educational resources is displayed
        resources = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(resources), 0, "No educational resources found.")

        # Attempt to upload a new educational resource
        # Note: The current implementation does not support uploading resources via UI, so this will fail
        self.fail("Upload educational resource functionality not implemented")

    def test_messaging_in_study_groups(self):
        # Login successfully and navigate to a study group
        # Note: The current implementation does not support messaging via UI, so this will fail
        self.fail("Messaging in study groups functionality not implemented")

    def test_user_logout(self):
        # Login successfully
        self.login("admin", "admin123")

        # Logout from the Dashboard Page
        # Note: The current implementation does not support logout via UI, so this will fail
        self.fail("Logout functionality not implemented")

    def test_navigate_back_to_dashboard(self):
        # Navigate to the Profile Page after logging in
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8553/profile')
        time.sleep(1)

        # Click the "Back to Dashboard" button
        # Note: The current implementation does not support navigating back to the dashboard via UI, so this will fail
        self.fail("Navigate back to dashboard functionality not implemented")

    def test_view_educational_resource_details(self):
        # Login successfully and navigate to the Resources Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8553/resources')
        time.sleep(1)

        # Click on a specific educational resource to view details
        # Note: The current implementation does not support viewing resource details via UI, so this will fail
        self.fail("View educational resource details functionality not implemented")

if __name__ == '__main__':
    unittest.main()
