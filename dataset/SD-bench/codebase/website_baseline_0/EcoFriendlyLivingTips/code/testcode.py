import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestEcoFriendlyLivingApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8533/')

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

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
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
        self.driver.find_element(By.LINK_TEXT, 'Introduction').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Introduction Page has loaded
        self.assertIn("Introduction to Eco-Friendly Living", self.driver.title)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting eco-friendly living tips
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows tips
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips), 0, "No tips found.")

        # Submit a new tip
        self.driver.find_element(By.NAME, 'title').send_keys("New Tip")
        self.driver.find_element(By.NAME, 'content').send_keys("This is a new eco-friendly tip.")
        self.driver.find_element(By.XPATH, '//button[text()="Add Tip"]').click()
        time.sleep(1)  # Wait for the tip to be added

        # Verify that the new tip is displayed on the Dashboard
        self.assertIn("New Tip", self.driver.page_source)

    def test_access_and_add_resources(self):
        # Functionalities 6: Test accessing and adding external resources
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows resources
        resources = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(resources), 0, "No resources found.")

        # Add a new resource
        self.driver.find_element(By.NAME, 'title').send_keys("New Resource")
        self.driver.find_element(By.NAME, 'url').send_keys("https://newresource.com")
        self.driver.find_element(By.XPATH, '//button[text()="Add Resource"]').click()
        time.sleep(1)  # Wait for the resource to be added

        # Verify that the new resource is displayed on the Dashboard
        self.assertIn("New Resource", self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8533/forum')
        time.sleep(1)  # Wait for the forum page to load

        # Verify that the forum posts are displayed
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No forum posts found.")

        # Submit a new forum post
        self.driver.find_element(By.NAME, 'content').send_keys("This is a new forum post.")
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        time.sleep(1)  # Wait for the post to be added

        # Verify that the new post is displayed in the forum
        self.assertIn("This is a new forum post.", self.driver.page_source)

    def test_profile_management(self):
        # Functionalities 8: Test profile management
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8533/profile')
        time.sleep(1)  # Wait for the profile page to load

        # Verify that the user's current profile information is displayed
        username_field = self.driver.find_element(By.NAME, 'username')
        self.assertEqual(username_field.get_attribute('value'), "admin")

        # Update profile information
        new_username = "admin_updated"
        username_field.clear()
        username_field.send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the profile to be updated

        # Verify that the profile information is updated
        self.assertIn("Dashboard", self.driver.title)

    def test_logout(self):
        # Functionalities 9: Test logging out
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_contact_support(self):
        # Functionalities 10: Test contact support
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8533/contact')
        time.sleep(1)  # Wait for the contact page to load

        # Fill out the contact form
        self.driver.find_element(By.NAME, 'message').send_keys("This is a support message.")
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()
        time.sleep(1)  # Wait for the message to be sent

        # Verify that a confirmation message is displayed
        self.assertIn("Your message has been sent successfully!", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
