import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestTravelMemoryShareApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8324/login')

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

    def test_user_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8324/register')
        
        # Verify Registration Page is displayed
        self.assertIn("Registration", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify registration success message
        self.assertIn("Registration successful", self.driver.page_source)

        # Attempt to register with an existing username
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("Username already exists", self.driver.page_source)

    def test_user_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8324/login')

        # Verify Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Login with valid credentials
        self.login("admin", "admin123")

        # Verify redirection to Dashboard Page
        self.assertIn("Album Gallery", self.driver.title)

        # Attempt login with invalid credentials
        self.login("invalid_user", "invalid_pass")

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_create_and_upload_travel_albums(self):
        # Functionality 3: Create and Upload Travel Albums
        self.login("admin", "admin123")

        # Verify Dashboard Page displays option to create album
        self.assertIn("Album Gallery", self.driver.title)

        # Attempt to create an album without filling required fields
        # (Assuming there's a form for creating albums, which is not implemented in the codebase)
        self.fail("Create album functionality not implemented")

    def test_customize_album_layout_and_design(self):
        # Functionality 4: Customize Album Layout and Design
        self.login("admin", "admin123")

        # Navigate to an existing album
        # (Assuming there's a way to navigate to albums, which is not implemented in the codebase)
        self.fail("Customize album functionality not implemented")

    def test_share_albums(self):
        # Functionality 5: Share Albums
        self.login("admin", "admin123")

        # Navigate to an existing album
        # (Assuming there's a way to share albums, which is not implemented in the codebase)
        self.fail("Share album functionality not implemented")

    def test_explore_and_view_albums_shared_by_others(self):
        # Functionality 6: Explore and View Albums Shared by Others
        self.login("admin", "admin123")

        # Navigate to the Explore Page
        # (Assuming there's an Explore Page, which is not implemented in the codebase)
        self.fail("Explore albums functionality not implemented")

    def test_interact_with_other_users(self):
        # Functionality 7: Interact with Other Users
        self.login("admin", "admin123")

        # Navigate to an album shared by another user
        # (Assuming interaction options are available, which is not implemented in the codebase)
        self.fail("Interact with users functionality not implemented")

    def test_follow_other_users(self):
        # Functionality 8: Follow Other Users
        self.login("admin", "admin123")

        # Navigate to a user's profile page
        # (Assuming there's a profile page, which is not implemented in the codebase)
        self.fail("Follow users functionality not implemented")

    def test_user_logout(self):
        # Functionality 9: User Logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to Login Page
        self.assertIn("Login", self.driver.title)

    def test_receive_updates_on_new_albums(self):
        # Functionality 10: Receive Updates on New Albums
        self.login("admin", "admin123")

        # Follow another user and log out
        # (Assuming follow functionality is available, which is not implemented in the codebase)
        self.fail("Receive updates functionality not implemented")

if __name__ == '__main__':
    unittest.main()
