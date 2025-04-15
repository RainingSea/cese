import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTravelMemoryShareApp(unittest.TestCase):

    def setUp(self):
        # Start the application server
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start

        # Initialize the webdriver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8326/')

    def tearDown(self):
        # Close the web driver session and stop the server
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
        self.driver.find_element(By.LINK_TEXT, "Register here").click()
        time.sleep(1)

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify successful registration redirects to login
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, "Register here").click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertIn("Username already exists", error_message)

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Login with valid credentials
        self.login("admin", "admin123")

        # Verify redirection to the Dashboard Page
        self.assertIn("Explore Albums", self.driver.page_source)

        # Logout to test invalid login
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Login with invalid credentials
        self.login("invalid_user", "wrong_password")

        # Verify error message for invalid credentials
        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertIn("Invalid username or password", error_message)

    def test_create_and_upload_travel_albums(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify the option to create a new travel album
        self.driver.find_element(By.LINK_TEXT, 'Create New Album').click()
        time.sleep(1)

        # Fill in album details and create album
        self.driver.find_element(By.NAME, 'title').send_keys("New Album")
        self.driver.find_element(By.NAME, 'is_public').click()
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        time.sleep(1)

        # Verify album creation
        self.assertIn("New Album", self.driver.page_source)

        # Attempt to create an album without filling required fields
        self.driver.find_element(By.LINK_TEXT, 'Create New Album').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        time.sleep(1)

        # Verify error message for missing fields
        self.assertIn("All required fields must be filled", self.driver.page_source)

    def test_customize_album_layout_and_design(self):
        # This functionality is not implemented in the codebase
        self.fail("Customize Album Layout and Design functionality not implemented")

    def test_share_albums(self):
        # This functionality is not implemented in the codebase
        self.fail("Share Albums functionality not implemented")

    def test_explore_and_view_albums_shared_by_others(self):
        # Login and navigate to the Explore Page
        self.login("admin", "admin123")

        # Verify a list of albums is displayed
        albums = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(albums), 0, "No albums found.")

        # Attempt to view a private album
        # This functionality is not fully implemented in the codebase
        self.fail("Viewing private albums functionality not fully implemented")

    def test_interact_with_other_users(self):
        # This functionality is not implemented in the codebase
        self.fail("Interact with Other Users functionality not implemented")

    def test_follow_other_users(self):
        # This functionality is not implemented in the codebase
        self.fail("Follow Other Users functionality not implemented")

    def test_user_logout(self):
        # Login and then logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8326/explore')
        self.assertIn("Login", self.driver.title)

    def test_receive_updates_on_new_albums(self):
        # This functionality is not implemented in the codebase
        self.fail("Receive Updates on New Albums functionality not implemented")

if __name__ == '__main__':
    unittest.main()
