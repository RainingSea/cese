import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestEcoFriendlyLivingTips(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')  # Replace with the actual port from main.py

    def tearDown(self):
        # Close the web driver session and the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_introduction(self):
        # Functionalities 4: Test viewing introduction after logging in
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/introduction')  # Assuming the introduction page URL
        self.assertIn("Introduction", self.driver.title)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting tips
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/tips')
        
        # Verify tips are displayed
        tips = self.driver.find_elements(By.TAG_NAME, 'li')  # Assuming tips are in <li> elements
        self.assertGreater(len(tips), 0, "No tips found.")

        # Submit a new tip
        self.driver.find_element(By.NAME, 'tip').send_keys("Reduce water usage.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()

        # Verify the new tip is displayed
        self.assertIn("Reduce water usage.", self.driver.page_source)

    def test_access_and_add_resources(self):
        # Functionalities 6: Test accessing and adding resources
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/resources')

        # Verify existing resources are displayed
        resources = self.driver.find_elements(By.TAG_NAME, 'li')  # Assuming resources are in <li> elements
        self.assertGreater(len(resources), 0, "No resources found.")

        # Add a new resource
        self.driver.find_element(By.NAME, 'url').send_keys("https://www.example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Add Resource"]').click()

        # Verify the new resource is displayed
        self.assertIn("https://www.example.com", self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/forum')

        # Verify forum posts are displayed
        posts = self.driver.find_elements(By.TAG_NAME, 'li')  # Assuming posts are in <li> elements
        self.assertGreater(len(posts), 0, "No forum posts found.")

        # Submit a new forum post
        self.driver.find_element(By.NAME, 'post').send_keys("This is a new forum post.")
        self.driver.find_element(By.XPATH, '//button[text()="Add Post"]').click()

        # Verify the new post is displayed
        self.assertIn("This is a new forum post.", self.driver.page_source)

    def test_profile_management(self):
        # Functionalities 8: Test profile management
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/profile')

        # Verify current profile information is displayed
        self.assertIn("admin", self.driver.page_source)  # Assuming username is displayed

        # Update profile information
        self.driver.find_element(By.NAME, 'username').clear()
        self.driver.find_element(By.NAME, 'username').send_keys("admin_updated")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()

        # Verify the updated profile information is displayed
        self.assertIn("admin_updated", self.driver.page_source)

    def test_user_logout(self):
        # Functionalities 9: Test user logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_contact_support(self):
        # Functionalities 10: Test contacting support
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/contact')

        # Fill out the contact form
        self.driver.find_element(By.NAME, 'message').send_keys("This is a test message.")
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()

        # Verify confirmation message is displayed
        self.assertIn("Message sent successfully", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
