import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestEcoFriendlyLivingTips(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8329/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
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
        self.assertIn("Welcome to EcoFriendlyLivingTips", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_tips(self):
        # Functionalities 5: Test viewing tips after logging in
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        self.assertIn("Eco-Friendly Living Tips", self.driver.page_source)

    def test_submit_tip(self):
        # Functionalities 5: Test submitting a new tip
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        
        new_tip = "Use reusable bags."
        self.driver.find_element(By.NAME, 'tip').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify the new tip is displayed
        self.assertIn(new_tip, self.driver.page_source)

    def test_view_resources(self):
        # Functionalities 6: Test viewing resources after logging in
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Resources').click()
        self.assertIn("External Resources", self.driver.page_source)

    def test_add_resource(self):
        # Functionalities 6: Test adding a new resource
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Resources').click()
        
        new_resource = "https://www.example.com"
        self.driver.find_element(By.NAME, 'resource').send_keys(new_resource)
        self.driver.find_element(By.XPATH, '//button[text()="Add"]').click()

        # Verify the new resource is displayed
        self.assertIn(new_resource, self.driver.page_source)

    def test_view_forum(self):
        # Functionalities 7: Test viewing forum posts after logging in
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.assertIn("Community Forum", self.driver.page_source)

    def test_submit_forum_post(self):
        # Functionalities 7: Test submitting a new forum post
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        
        new_post = "What are your favorite eco-friendly products?"
        self.driver.find_element(By.NAME, 'post').send_keys(new_post)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify the new post is displayed
        self.assertIn(new_post, self.driver.page_source)

    def test_contact_support(self):
        # Functionalities 10: Test submitting a contact form
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Contact').click()
        
        self.driver.find_element(By.NAME, 'name').send_keys("Test User")
        self.driver.find_element(By.NAME, 'email').send_keys("test@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("This is a test message.")
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()

        # Verify a confirmation message is displayed
        self.assertIn("Your message has been sent successfully.", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
