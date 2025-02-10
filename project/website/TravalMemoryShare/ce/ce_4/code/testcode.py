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
        self.driver.get('http://localhost:8657/')  # Navigate to the login page

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
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then click the "Register" button
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify that an error message is displayed
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")
        self.assertIn("Create Album", self.driver.page_source)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8657/')
        self.login("invalid_user", "wrong_password")
        self.assertIn("Login", self.driver.title)

    def test_create_and_upload_travel_albums(self):
        # Login successfully
        self.login("admin", "admin123")

        # Navigate to the Dashboard Page and create a new album
        self.driver.find_element(By.LINK_TEXT, 'Create Album').click()
        self.assertIn("Create Album", self.driver.title)

        # Fill in the album details and upload images
        self.driver.find_element(By.NAME, 'title').send_keys("My Album")
        self.driver.find_element(By.NAME, 'photos').send_keys("photo1.jpg,photo2.jpg")
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        time.sleep(1)

        # Verify the album is created successfully
        self.assertIn("Explore Albums", self.driver.title)

        # Attempt to create an album without filling in required fields
        self.driver.find_element(By.LINK_TEXT, 'Create Album').click()
        self.driver.find_element(By.XPATH, '//button[text()="Create Album"]').click()
        time.sleep(1)

        # Verify that an error message is displayed
        self.assertIn("Create Album", self.driver.title)

    def test_explore_and_view_albums_shared_by_others(self):
        # Login successfully
        self.login("admin", "admin123")

        # Navigate to the Explore Page
        self.driver.find_element(By.LINK_TEXT, 'Explore Albums').click()
        self.assertIn("Explore Albums", self.driver.title)

        # Click on an album to view its details
        albums = self.driver.find_elements(By.TAG_NAME, 'li')
        if albums:
            albums[0].click()
            self.assertIn("Photos", self.driver.page_source)
        else:
            self.fail("No albums found to explore.")

    def test_user_logout(self):
        # Login successfully
        self.login("admin", "admin123")

        # Logout from the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8657/explore')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
