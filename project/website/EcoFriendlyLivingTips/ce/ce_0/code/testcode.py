import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestEcoFriendlyLivingApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8327/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration_page(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Create Account').click()
        self.assertIn("Create Account", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Create Account').click()
        
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Create Account"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_tips(self):
        # Functionalities 4: Test viewing tips after logging in
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Resources').click()
        self.assertIn("External Resources", self.driver.title)

    def test_submit_tip(self):
        # Functionalities 5: Test submitting a new tip
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Dashboard').click()

        new_tip = "Plant more trees."
        self.driver.find_element(By.NAME, 'tip').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify the new tip is displayed
        self.assertIn(new_tip, self.driver.page_source)

    def test_access_resources(self):
        # Functionalities 6: Test accessing resources after logging in
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Resources').click()
        self.assertIn("External Resources", self.driver.page_source)

    def test_add_resource(self):
        # Functionalities 6: Test adding a new resource
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Resources').click()

        new_resource = "www.newresource.com"
        self.driver.find_element(By.NAME, 'resource').send_keys(new_resource)
        self.driver.find_element(By.XPATH, '//button[text()="Add Resource"]').click()

        # Verify the new resource is displayed
        self.assertIn(new_resource, self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Community Forum').click()
        
        new_post = "This is a new forum post."
        self.driver.find_element(By.NAME, 'post').send_keys(new_post)
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()

        # Verify the new post is displayed
        self.assertIn(new_post, self.driver.page_source)

    def test_access_profile(self):
        # Functionalities 8: Test accessing the profile page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.assertIn("User Profile", self.driver.page_source)

    def test_contact_support(self):
        # Functionalities 10: Test contacting support
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Contact').click()

        # Simulate filling out the contact form
        self.driver.find_element(By.NAME, 'contact_message').send_keys("Need help with my account.")
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()

        # Verify a confirmation message is displayed
        self.assertIn("Message sent successfully", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
