import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestSocialShareApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8247/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8247/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8247/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Check for error message
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Feed", self.driver.title)  # Check if redirected to Feed Page

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8247/')
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_profile_creation_and_update(self):
        # Functionality 3: Profile Creation and Update
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8247/profile')  # Navigate to Profile Page
        self.assertIn("User Profile", self.driver.title)

        # Update bio
        bio_text = "This is my bio."
        self.driver.find_element(By.NAME, 'bio').send_keys(bio_text)
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()

        # Verify the profile is updated
        self.assertIn("Profile updated successfully", self.driver.page_source)

        # Attempt to leave bio empty
        self.driver.find_element(By.NAME, 'bio').clear()  # Clear bio
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        self.assertIn("Bio cannot be empty", self.driver.page_source)

    def test_content_discovery(self):
        # Functionality 5: Content Discovery
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8247/feed')  # Navigate to Feed Page
        self.assertIn("Content Feed", self.driver.title)

        # Check if articles are displayed
        articles = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(articles), 0, "No articles found.")

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8247/')  # Navigate to Login Page
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
