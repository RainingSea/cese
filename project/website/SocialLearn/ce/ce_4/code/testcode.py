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
        self.driver.get('http://localhost:8639/') 

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
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Expectation: Error message for existing username (not implemented)
        self.fail("Error message for existing username not implemented")

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Profile", self.driver.title)

        # Invalid login
        self.driver.get('http://localhost:8639/')
        self.login("invalid_user", "invalid_pass")
        self.assertIn("Login", self.driver.title)

    def test_user_profile_management(self):
        # Login and navigate to Profile Page
        self.login("admin", "admin123")
        self.assertIn("Profile", self.driver.title)

        # Update profile with new interests
        self.driver.find_element(By.NAME, 'interests').clear()
        self.driver.find_element(By.NAME, 'interests').send_keys("science,math,art")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)

        # Expectation: Confirmation message (not implemented)
        self.fail("Confirmation message for profile update not implemented")

    def test_join_study_groups(self):
        # Login and navigate to Study Groups Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Study Groups').click()
        self.assertIn("Study Groups", self.driver.title)

        # Expectation: Join study group (not implemented)
        self.fail("Join study group functionality not implemented")

    def test_share_and_access_resources(self):
        # Login and navigate to Resources Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Resources').click()
        self.assertIn("Resources", self.driver.title)

        # Upload a new resource
        self.driver.find_element(By.NAME, 'title').send_keys("New Resource")
        self.driver.find_element(By.NAME, 'link').send_keys("https://example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Share Resource"]').click()
        time.sleep(1)

        # Expectation: Resource uploaded successfully (not implemented)
        self.fail("Resource upload confirmation not implemented")

    def test_messaging_in_study_groups(self):
        # Login and navigate to Messaging Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Messaging').click()
        self.assertIn("Messaging", self.driver.title)

        # Send a message
        self.driver.find_element(By.NAME, 'receiver').send_keys("user1")
        self.driver.find_element(By.NAME, 'content').send_keys("Hello!")
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()
        time.sleep(1)

        # Expectation: Message sent confirmation (not implemented)
        self.fail("Message sent confirmation not implemented")

    def test_user_logout(self):
        # Login and logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Login and navigate to Profile Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.assertIn("Profile", self.driver.title)

        # Expectation: Navigate back to Dashboard (not implemented)
        self.fail("Back to Dashboard functionality not implemented")

    def test_view_educational_resource_details(self):
        # Login and navigate to Resources Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Resources').click()
        self.assertIn("Resources", self.driver.title)

        # Expectation: View resource details (not implemented)
        self.fail("View resource details functionality not implemented")

if __name__ == '__main__':
    unittest.main()
