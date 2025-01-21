import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestEcoFriendlyLivingApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:9032/')  # Access the login page

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
        # Assuming there's a "Register here" link on the login page
        try:
            self.driver.find_element(By.LINK_TEXT, 'Register here').click()
            time.sleep(1)  # Wait for the next page to load

            # Verify that the Registration Page has loaded
            self.assertIn("Register", self.driver.title)
        except:
            self.fail("Registration page navigation not implemented")

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        # Assuming there's a registration page and form
        try:
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
        except:
            self.fail("User registration not implemented")

    def test_view_introduction(self):
        # Functionalities 4: Test viewing introduction to eco-friendly living
        self.login("admin", "admin123")
        # Assuming introduction content is part of the dashboard
        self.assertIn("Eco-Friendly Tips", self.driver.page_source)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting eco-friendly living tips
        self.login("admin", "admin123")

        # Verify that tips are displayed
        self.assertIn("Eco-Friendly Tips", self.driver.page_source)

        # Submit a new tip
        new_tip = "Use solar panels"
        self.driver.find_element(By.NAME, 'new_tip').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be submitted

        # Verify the new tip is displayed
        self.assertIn(new_tip, self.driver.page_source)

    def test_access_and_add_resources(self):
        # Functionalities 6: Test accessing and adding external resources
        self.login("admin", "admin123")

        # Verify that resources are displayed
        self.assertIn("Resources", self.driver.page_source)

        # Add a new resource
        new_resource = "https://www.example.com"
        self.driver.find_element(By.NAME, 'new_resource').send_keys(new_resource)
        self.driver.find_element(By.XPATH, '//button[text()="Add Resource"]').click()
        time.sleep(1)  # Wait for the resource to be added

        # Verify the new resource is displayed
        self.assertIn(new_resource, self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "admin123")

        # Navigate to the forum page
        self.driver.get('http://localhost:9032/forum')
        time.sleep(1)  # Wait for the forum page to load

        # Verify that forum posts are displayed
        self.assertIn("Community Forum", self.driver.page_source)

        # Submit a new forum post
        new_post = "How can I start composting?"
        self.driver.find_element(By.NAME, 'content').send_keys(new_post)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the post to be submitted

        # Verify the new post is displayed
        self.assertIn(new_post, self.driver.page_source)

    def test_profile_management(self):
        # Functionalities 8: Test profile management
        self.fail("Profile management not implemented")

    def test_logout(self):
        # Functionalities 9: Test user logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_contact_support(self):
        # Functionalities 10: Test contact support
        self.driver.get('http://localhost:9032/contact')
        time.sleep(1)  # Wait for the contact page to load

        # Fill out the contact form
        message = "I need help with my account."
        self.driver.find_element(By.NAME, 'message').send_keys(message)
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()
        time.sleep(1)  # Wait for the message to be sent

        # Verify a confirmation message is displayed
        self.assertIn("Message sent", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
