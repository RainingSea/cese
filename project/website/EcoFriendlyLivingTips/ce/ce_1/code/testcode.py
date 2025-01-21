import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestEcoFriendlyLivingTips(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:9029/') 

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

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_introduction(self):
        # Functionalities 4: Test viewing introduction to Eco-Friendly Living
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows introduction content
        self.assertIn("Eco-Friendly Tips", self.driver.page_source)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting eco-friendly tips
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit a Tip').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the tips are displayed
        self.assertIn("Submit Eco-Friendly Tip", self.driver.page_source)

        # Submit a new tip
        self.driver.find_element(By.NAME, 'title').send_keys("New Tip")
        self.driver.find_element(By.NAME, 'content').send_keys("This is a new eco-friendly tip.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be submitted

        # Verify that the new tip is displayed
        self.assertIn("New Tip", self.driver.page_source)

    def test_access_and_add_resources(self):
        # Functionalities 6: Test accessing and adding external resources
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Resources').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that resources are displayed
        self.assertIn("Existing Resources", self.driver.page_source)

        # Add a new resource
        self.driver.find_element(By.NAME, 'title').send_keys("New Resource")
        self.driver.find_element(By.NAME, 'link').send_keys("https://newresource.com")
        self.driver.find_element(By.XPATH, '//button[text()="Add Resource"]').click()
        time.sleep(1)  # Wait for the resource to be added

        # Verify that the new resource is displayed
        self.assertIn("New Resource", self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that forum posts are displayed
        self.assertIn("Community Forum", self.driver.page_source)

        # Submit a new forum post
        self.driver.find_element(By.NAME, 'content').send_keys("This is a new forum post.")
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        time.sleep(1)  # Wait for the post to be submitted

        # Verify that the new post is displayed
        self.assertIn("This is a new forum post.", self.driver.page_source)

    def test_profile_management(self):
        # Functionalities 8: Test profile management (not implemented)
        self.fail("Profile management functionality is not implemented.")

    def test_logout(self):
        # Functionalities 9: Test logging out
        self.login("admin", "admin123")
        # Logout functionality is not implemented in the codebase
        self.fail("Logout functionality is not implemented.")

    def test_contact_support(self):
        # Functionalities 10: Test contact support
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Contact').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the contact form
        self.driver.find_element(By.NAME, 'name').send_keys("Test User")
        self.driver.find_element(By.NAME, 'email').send_keys("testuser@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("This is a test message.")
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()
        time.sleep(1)  # Wait for the message to be sent

        # Verify that a confirmation message is displayed (not implemented)
        self.fail("Contact support confirmation message functionality is not implemented.")

if __name__ == '__main__':
    unittest.main()
