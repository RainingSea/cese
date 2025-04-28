import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestEcoFriendlyLivingTips(unittest.TestCase):

    def setUp(self):
        # Start the server and initialize the webdriver
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/') 

    def tearDown(self):
        # Close the web driver session and terminate the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration_page(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Create Account').click()
        self.assertIn("Create Account", self.driver.title)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting eco-friendly living tips
        self.login("admin", "admin123")
        
        # View tips
        self.driver.get('http://localhost:8000/tips')
        tips_displayed = self.driver.find_element(By.ID, 'tips').text
        self.assertIn("Reduce, reuse, recycle.", tips_displayed)

        # Submit a new tip
        new_tip = "Plant more trees."
        self.driver.find_element(By.NAME, 'tip').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//input[@value="Submit Tip"]').click()

        # Verify the new tip is displayed
        tips_displayed = self.driver.find_element(By.ID, 'tips').text
        self.assertIn(new_tip, tips_displayed)

    def test_access_and_add_external_resources(self):
        # Functionalities 6: Test accessing and adding external resources
        self.login("admin", "admin123")
        
        # View resources
        self.driver.get('http://localhost:8000/resources')
        resources_displayed = self.driver.find_element(By.ID, 'resources').text
        self.assertIn("https://www.epa.gov/recycle", resources_displayed)

        # Add a new resource
        new_resource = "https://www.greenpeace.org"
        self.driver.find_element(By.NAME, 'resource').send_keys(new_resource)
        self.driver.find_element(By.XPATH, '//input[@value="Add Resource"]').click()

        # Verify the new resource is displayed
        resources_displayed = self.driver.find_element(By.ID, 'resources').text
        self.assertIn(new_resource, resources_displayed)

    def test_participate_in_community_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "admin123")
        
        # View forum posts
        self.driver.get('http://localhost:8000/forum')
        forum_posts_displayed = self.driver.find_element(By.ID, 'posts').text
        self.assertIn("Welcome to the community forum!", forum_posts_displayed)

        # Submit a new forum post
        new_post = "Let's share more eco-friendly tips!"
        self.driver.find_element(By.NAME, 'post').send_keys(new_post)
        self.driver.find_element(By.XPATH, '//input[@value="Add Post"]').click()

        # Verify the new post is displayed
        forum_posts_displayed = self.driver.find_element(By.ID, 'posts').text
        self.assertIn(new_post, forum_posts_displayed)

    def test_profile_management(self):
        # Functionalities 8: Test profile management
        self.login("admin", "admin123")
        
        # Access profile page
        self.driver.get('http://localhost:8000/profile')
        self.assertIn("User Profile", self.driver.title)

        # Update profile information
        updated_username = "admin_updated"
        updated_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(updated_username)
        self.driver.find_element(By.NAME, 'password').send_keys(updated_password)
        self.driver.find_element(By.XPATH, '//input[@value="Update Profile"]').click()

        # Verify the profile information is updated
        self.assertIn(updated_username, self.driver.page_source)

    def test_user_logout(self):
        # Functionalities 9: Test user logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_contact_support(self):
        # Functionalities 10: Test contact support functionality
        self.login("admin", "admin123")
        
        # Access contact support page
        self.driver.get('http://localhost:8000/contact')
        self.driver.find_element(By.NAME, 'message').send_keys("Need help with my account.")
        self.driver.find_element(By.XPATH, '//input[@value="Send"]').click()

        # Verify confirmation message
        self.assertIn("Your message has been sent.", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
