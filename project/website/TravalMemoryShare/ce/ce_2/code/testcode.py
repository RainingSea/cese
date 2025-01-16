import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelMemoryShareApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8655/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()

        # Verify that the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then click the "Register" button
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify that an error message is displayed
        self.assertIn("Register", self.driver.title)  # Assuming it stays on the register page

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and the user is redirected to the Dashboard Page
        self.assertIn("Gallery", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8655/')
        self.login("invalid_user", "invalid_pass")

        # Verify that an error message is displayed
        self.assertIn("Login", self.driver.title)  # Assuming it redirects back to login page

    def test_create_and_upload_travel_albums(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify that the user can see an option to create a new travel album
        self.assertIn("Gallery", self.driver.title)

        # Attempt to create an album without filling in required fields
        # This functionality is not implemented in the codebase, so it will fail
        self.fail("Create album functionality not implemented")

    def test_customize_album_layout_and_design(self):
        # This functionality is not implemented in the codebase, so it will fail
        self.fail("Customize album layout functionality not implemented")

    def test_share_albums(self):
        # This functionality is not implemented in the codebase, so it will fail
        self.fail("Share albums functionality not implemented")

    def test_explore_and_view_albums_shared_by_others(self):
        # This functionality is not implemented in the codebase, so it will fail
        self.fail("Explore and view albums functionality not implemented")

    def test_interact_with_other_users(self):
        # This functionality is not implemented in the codebase, so it will fail
        self.fail("Interact with other users functionality not implemented")

    def test_follow_other_users(self):
        # This functionality is not implemented in the codebase, so it will fail
        self.fail("Follow other users functionality not implemented")

    def test_user_logout(self):
        # Login and then logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_receive_updates_on_new_albums(self):
        # This functionality is not implemented in the codebase, so it will fail
        self.fail("Receive updates on new albums functionality not implemented")

if __name__ == '__main__':
    unittest.main()
