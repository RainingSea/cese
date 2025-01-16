import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestTravelMemoryShareApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8557')

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
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)

        # Enter a valid username and password, then click "Register"
        self.driver.find_element(By.NAME, 'username').send_keys('newuser')
        self.driver.find_element(By.NAME, 'password').send_keys('newpass')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify registration success
        self.assertIn('Login', self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn('Registration failed', self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8557')
        time.sleep(1)

        # Enter valid credentials
        self.login('admin', 'admin123')

        # Verify redirection to the Dashboard Page
        self.assertIn('Albums', self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8557')
        self.login('invalid', 'invalid')

        # Verify error message for invalid credentials
        self.assertIn('Login failed', self.driver.page_source)

    def test_create_and_upload_travel_albums(self):
        # Login and navigate to the Dashboard Page
        self.login('admin', 'admin123')

        # Create a new album
        self.driver.find_element(By.NAME, 'title').send_keys('New Album')
        self.driver.find_element(By.NAME, 'photos').send_keys('photo1.jpg,photo2.jpg')
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        time.sleep(1)

        # Verify album creation success
        self.assertIn('Album created successfully', self.driver.page_source)

        # Attempt to create an album without filling required fields
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        time.sleep(1)

        # Verify error message for missing fields
        self.assertIn('required', self.driver.page_source)

    def test_customize_album_layout_and_design(self):
        # Login and navigate to an existing album
        self.login('admin', 'admin123')
        self.driver.find_element(By.LINK_TEXT, 'Customize').click()
        time.sleep(1)

        # Change layout and save changes
        self.driver.find_element(By.ID, 'layout').send_keys('list')
        self.driver.find_element(By.XPATH, '//button[text()="Apply"]').click()
        time.sleep(1)

        # Verify customization success
        self.assertIn('customized successfully', self.driver.page_source)

    def test_share_albums(self):
        # Login and navigate to an existing album
        self.login('admin', 'admin123')
        self.driver.find_element(By.LINK_TEXT, 'Share').click()
        time.sleep(1)

        # Verify sharing success
        self.assertIn('shared successfully', self.driver.page_source)

    def test_explore_and_view_albums_shared_by_others(self):
        # Login and navigate to the Explore Page
        self.login('admin', 'admin123')
        self.driver.find_element(By.LINK_TEXT, 'Explore Shared Albums').click()
        time.sleep(1)

        # Verify shared albums are displayed
        self.assertIn('Explore Shared Albums', self.driver.title)

    def test_interact_with_other_users(self):
        # Login and navigate to an album shared by another user
        self.login('admin', 'admin123')
        self.driver.find_element(By.LINK_TEXT, 'Interact').click()
        time.sleep(1)

        # Verify interaction success
        self.assertIn('interacted with', self.driver.page_source)

    def test_follow_other_users(self):
        # Login and navigate to a user's profile page
        self.login('admin', 'admin123')
        self.driver.find_element(By.LINK_TEXT, 'Follow').click()
        time.sleep(1)

        # Verify follow success
        self.assertIn('following', self.driver.page_source)

    def test_user_logout(self):
        # Login and logout
        self.login('admin', 'admin123')
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn('Login', self.driver.title)

    def test_receive_updates_on_new_albums(self):
        # This functionality is not implemented in the codebase
        self.fail("Receive updates on new albums functionality not implemented")

if __name__ == '__main__':
    unittest.main()
