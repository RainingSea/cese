import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestSocialLearnApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8637/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)

        # Check for error message (not implemented in the codebase)
        self.fail("Error message for existing username not implemented")

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")
        self.assertIn("Profile", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8637/')
        self.login("invalid_user", "invalid_pass")
        self.assertIn("Login", self.driver.title)

    def test_user_profile_management(self):
        # Login successfully and navigate to the Profile Page
        self.login("admin", "admin123")
        self.assertIn("Profile", self.driver.title)

        # Update the profile with new areas of interest and save changes
        self.driver.find_element(By.NAME, 'interests').send_keys("Python, Flask")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)

        # Check for confirmation message (not implemented in the codebase)
        self.fail("Profile update confirmation message not implemented")

    def test_join_study_groups(self):
        # Login successfully and navigate to the Study Groups Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Study Groups').click()
        self.assertIn("Study Groups", self.driver.title)

        # Attempt to join a study group (not implemented in the codebase)
        self.fail("Join study group functionality not implemented")

    def test_share_and_access_educational_resources(self):
        # Login successfully and navigate to the Resources Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Resources').click()
        self.assertIn("Resources", self.driver.title)

        # Upload a new educational resource
        self.driver.find_element(By.NAME, 'title').send_keys("New Resource")
        self.driver.find_element(By.NAME, 'link').send_keys("https://example.com")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)

        # Verify the resource appears in the list
        self.assertIn("New Resource", self.driver.page_source)

    def test_messaging_in_study_groups(self):
        # Login successfully and navigate to the Messages Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Messages').click()
        self.assertIn("Messages", self.driver.title)

        # Send a message
        self.driver.find_element(By.NAME, 'receiver').send_keys("user1")
        self.driver.find_element(By.NAME, 'content').send_keys("Hello!")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)

        # Verify the message appears in the chat history
        self.assertIn("Hello!", self.driver.page_source)

    def test_user_logout(self):
        # Login and then logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Navigate to the Profile Page after logging in
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.assertIn("Profile", self.driver.title)

        # Click the "Back to Dashboard" button (not implemented in the codebase)
        self.fail("Back to Dashboard functionality not implemented")

    def test_view_educational_resource_details(self):
        # Login successfully and navigate to the Resources Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Resources').click()
        self.assertIn("Resources", self.driver.title)

        # Click on a specific educational resource to view details
        self.driver.find_element(By.LINK_TEXT, 'Python Programming').click()
        time.sleep(1)

        # Verify the details are displayed (not implemented in the codebase)
        self.fail("View educational resource details functionality not implemented")

if __name__ == '__main__':
    unittest.main()
