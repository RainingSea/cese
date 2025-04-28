import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestSocialShareApp(unittest.TestCase):

    def setUp(self):
        # Start the main application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the actual port

    def tearDown(self):
        # Close the web driver session and terminate the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:5000/login')  # Navigate to login page
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:5000/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.ID, 'username').send_keys(new_username)
        self.driver.find_element(By.ID, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify registration success
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:5000/register')  # Navigate to registration page
        self.driver.find_element(By.ID, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.ID, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:5000/login')  # Navigate to login page
        self.driver.find_element(By.ID, 'username').send_keys("admin")
        self.driver.find_element(By.ID, 'password').send_keys("wrongpassword")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_profile_update(self):
        # Functionality 3: Profile Creation and Update
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/profile')  # Navigate to profile page
        self.assertIn("Profile", self.driver.title)

        # Update bio
        self.driver.find_element(By.ID, 'bio').send_keys("Updated bio")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify profile update success
        self.assertIn("Profile updated successfully", self.driver.page_source)

        # Attempt to update with empty bio
        self.driver.find_element(By.ID, 'bio').clear()  # Clear the bio field
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for empty bio
        self.assertIn("Bio cannot be empty", self.driver.page_source)

    def test_content_upload(self):
        # Functionality 4: Content Upload and Sharing
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/upload')  # Navigate to content upload page
        self.assertIn("Upload Article", self.driver.title)

        # Upload a valid article
        self.driver.find_element(By.ID, 'title').send_keys("New Article")
        self.driver.find_element(By.ID, 'content').send_keys("This is the content of the new article.")
        self.driver.find_element(By.XPATH, '//button[text()="Share Article"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify article upload success
        self.assertIn("Article shared successfully", self.driver.page_source)

        # Attempt to upload an article with empty title
        self.driver.find_element(By.ID, 'title').clear()  # Clear the title field
        self.driver.find_element(By.ID, 'content').send_keys("Content without title.")
        self.driver.find_element(By.XPATH, '//button[text()="Share Article"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for empty title
        self.assertIn("Title cannot be empty", self.driver.page_source)

    def test_content_discovery(self):
        # Functionality 5: Content Discovery
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/feed')  # Navigate to discovery page
        self.assertIn("Feed", self.driver.title)

        # Verify that articles are displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'li')  # Assuming articles are in a list
        self.assertGreater(len(articles), 0, "No articles found.")

    def test_interact_with_content(self):
        # Functionality 6: Interacting with Content
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/feed')  # Navigate to discovery page
        self.assertIn("Feed", self.driver.title)

        # Like an article
        self.driver.find_element(By.XPATH, '//button[text()="Like"]').click()
        time.sleep(1)  # Wait for the action to process
        self.assertIn("Like count increased", self.driver.page_source)

        # Leave a comment
        self.driver.find_element(By.ID, 'comment').send_keys("Great article!")
        self.driver.find_element(By.XPATH, '//button[text()="Comment"]').click()
        time.sleep(1)  # Wait for the action to process
        self.assertIn("Comment added successfully", self.driver.page_source)

        # Attempt to like the same article again
        self.driver.find_element(By.XPATH, '//button[text()="Like"]').click()
        time.sleep(1)  # Wait for the action to process
        self.assertIn("Cannot like the same article multiple times", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
