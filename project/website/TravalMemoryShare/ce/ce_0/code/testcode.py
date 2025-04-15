import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTravelMemoryShareApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8322/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and stop the application
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
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then click "Register"
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify registration success
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("Username already exists.", self.driver.page_source)

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify redirection to the Dashboard Page
        self.assertIn("Create Album", self.driver.page_source)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8322/')  # Navigate back to login page
        self.login("invalid_user", "invalid_pass")

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials.", self.driver.page_source)

    def test_create_and_upload_travel_albums(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify option to create a new travel album
        self.assertIn("Create Album", self.driver.page_source)

        # Click on "Create Album", fill in the album details, and submit
        self.driver.find_element(By.LINK_TEXT, 'Create Album').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'title').send_keys("My Album")
        self.driver.find_element(By.NAME, 'description').send_keys("Album Description")
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        time.sleep(1)

        # Verify album creation success
        self.assertIn("Album created successfully!", self.driver.page_source)

        # Attempt to create an album without filling in required fields
        self.driver.find_element(By.LINK_TEXT, 'Create Album').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        time.sleep(1)

        # Verify error message for missing fields
        self.assertIn("This field is required.", self.driver.page_source)

    def test_customize_album_layout_and_design(self):
        # Functionality not implemented
        self.fail("Customize Album Layout and Design functionality not implemented")

    def test_share_albums(self):
        # Functionality not implemented
        self.fail("Share Albums functionality not implemented")

    def test_explore_and_view_albums_shared_by_others(self):
        # Functionality not implemented
        self.fail("Explore and View Albums Shared by Others functionality not implemented")

    def test_interact_with_other_users(self):
        # Functionality not implemented
        self.fail("Interact with Other Users functionality not implemented")

    def test_follow_other_users(self):
        # Functionality not implemented
        self.fail("Follow Other Users functionality not implemented")

    def test_user_logout(self):
        # Login and then logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8322/album/create')
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_receive_updates_on_new_albums(self):
        # Functionality not implemented
        self.fail("Receive Updates on New Albums functionality not implemented")

if __name__ == '__main__':
    unittest.main()
