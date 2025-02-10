import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTravelMemoryShareApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8653/')  # Navigate to the login page

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
        # Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Enter registration details
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check for error message
        self.assertIn("username is already taken", self.driver.page_source)

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "admin123")

        # Verify redirection to the explore page
        self.assertIn("Explore Albums", self.driver.title)

        # Test invalid login
        self.driver.get('http://localhost:8653/')  # Navigate back to login page
        self.login("invalid_user", "invalid_pass")

        # Check for error message
        self.assertIn("invalid credentials", self.driver.page_source)

    def test_create_and_upload_travel_albums(self):
        # Test creating and uploading travel albums
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create Album').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill in album details
        self.driver.find_element(By.NAME, 'title').send_keys('My Album')
        self.driver.find_element(By.NAME, 'images').send_keys('image1.jpg,image2.jpg')
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify album creation
        self.assertIn("My Album", self.driver.page_source)

        # Attempt to create an album without required fields
        self.driver.find_element(By.LINK_TEXT, 'Create Album').click()
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check for error message
        self.assertIn("all required fields must be filled", self.driver.page_source)

    def test_customize_album_layout_and_design(self):
        # Test customizing album layout and design
        self.fail("not implemented")

    def test_share_albums(self):
        # Test sharing albums
        self.fail("not implemented")

    def test_explore_and_view_albums_shared_by_others(self):
        # Test exploring and viewing albums shared by others
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Explore').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify albums are displayed
        albums = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(albums), 0, "No albums found.")

        # Attempt to view a private album
        self.fail("not implemented")

    def test_interact_with_other_users(self):
        # Test interacting with other users
        self.fail("not implemented")

    def test_follow_other_users(self):
        # Test following other users
        self.fail("not implemented")

    def test_user_logout(self):
        # Test user logout functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the explore page after logging out
        self.driver.get('http://localhost:8653/explore')
        self.assertIn("Login", self.driver.title)

    def test_receive_updates_on_new_albums(self):
        # Test receiving updates on new albums
        self.fail("not implemented")

if __name__ == '__main__':
    unittest.main()
