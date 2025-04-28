import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestSocialShareApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8418/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8418/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8418/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Discovery", self.driver.title)  # Check if redirected to Discovery Page

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8418/')
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_profile_creation_and_update(self):
        # Functionality 3: Profile Creation and Update
        self.login("admin", "admin123")  # Login successfully
        self.driver.get('http://localhost:8418/profile/admin')  # Navigate to Profile Page
        self.assertIn("Profile", self.driver.title)

        # Update bio
        bio = "This is my updated bio."
        self.driver.find_element(By.NAME, 'bio').send_keys(bio)
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the update to process

        # Verify that the profile is updated
        self.assertIn("Profile updated successfully", self.driver.page_source)

        # Attempt to leave bio empty
        self.driver.find_element(By.NAME, 'bio').clear()  # Clear the bio field
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the update to process

        # Verify error message for empty bio
        self.assertIn("Bio cannot be empty", self.driver.page_source)

    def test_content_upload_and_sharing(self):
        # Functionality 4: Content Upload and Sharing
        self.login("admin", "admin123")  # Login successfully
        self.driver.get('http://localhost:8418/share_article')  # Navigate to content upload page
        self.assertIn("Share Article", self.driver.title)

        # Share a valid article
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'content').send_keys("This is a new article.")
        self.driver.find_element(By.XPATH, '//button[text()="Share"]').click()
        time.sleep(1)  # Wait for the article to be shared

        # Verify that the article is shared successfully
        self.assertIn("Article shared successfully", self.driver.page_source)

        # Attempt to share an article with empty content
        self.driver.find_element(By.NAME, 'content').clear()  # Clear the content field
        self.driver.find_element(By.XPATH, '//button[text()="Share"]').click()
        time.sleep(1)  # Wait for the attempt to process

        # Verify error message for empty content
        self.assertIn("Content cannot be empty", self.driver.page_source)

    def test_content_discovery(self):
        # Functionality 5: Content Discovery
        self.login("admin", "admin123")  # Login successfully
        self.driver.get('http://localhost:8418/discovery')  # Navigate to discovery page
        self.assertIn("Articles", self.driver.title)

        # Verify that articles are displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

    def test_interacting_with_content(self):
        # Functionality 6: Interacting with Content
        self.login("admin", "admin123")  # Login successfully
        self.driver.get('http://localhost:8418/discovery')  # Navigate to discovery page

        # Simulate liking an article
        # Assuming there's a like button for each article
        self.driver.find_element(By.XPATH, '//button[text()="Like"]').click()
        time.sleep(1)  # Wait for the like action to process

        # Verify that the like count increases
        self.assertIn("Liked", self.driver.page_source)

        # Simulate commenting on an article
        self.driver.find_element(By.NAME, 'comment').send_keys("Great article!")
        self.driver.find_element(By.XPATH, '//button[text()="Comment"]').click()
        time.sleep(1)  # Wait for the comment action to process

        # Verify that the comment is displayed
        self.assertIn("Great article!", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Login successfully
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the logout to process

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
