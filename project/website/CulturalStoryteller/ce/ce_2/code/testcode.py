import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCulturalStorytellerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8309/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.get('http://localhost:8309/register')
        
        # Verify that the Registration Page is displayed
        self.assertIn("Registration", self.driver.title)

        # Enter a valid username and password, then submit the registration form
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8309/register')
        self.driver.find_element(By.NAME, 'username').send_keys("user1")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("test_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Registration Failed", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8309/')

        # Enter valid credentials and log in
        self.login("user1", "user123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Stories", self.driver.title)

        # Attempt to log in with invalid credentials
        self.driver.get('http://localhost:8309/')
        self.login("user1", "wrong_password")

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_explore_stories(self):
        # Log in successfully
        self.login("user1", "user123")

        # Verify that the Dashboard Page shows stories
        self.assertIn("Stories", self.driver.page_source)

        # Click on a story title
        self.driver.find_element(By.LINK_TEXT, "Story Title 1").click()

        # Verify that the Story Details Page is displayed
        self.assertIn("Story Details", self.driver.title)

    def test_view_story_details(self):
        # Log in successfully
        self.login("user1", "user123")

        # Click on a story from the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, "Story Title 1").click()

        # Verify that the Story Details Page is displayed with the full text
        self.assertIn("This is the text of story 1.", self.driver.page_source)

        # Check for the presence of the 'Add to Bookmarks' button
        self.assertIn("Add to Bookmarks", self.driver.page_source)

    def test_bookmark_stories(self):
        # Log in successfully
        self.login("user1", "user123")

        # Navigate to the Story Details Page
        self.driver.find_element(By.LINK_TEXT, "Story Title 1").click()

        # Click the 'Add to Bookmarks' button
        self.driver.find_element(By.XPATH, '//button[text()="Add to Bookmarks"]').click()

        # Verify that the story is added to bookmarks
        self.driver.get('http://localhost:8309/bookmarks')
        self.assertIn("Story Title 1", self.driver.page_source)

    def test_view_bookmarked_stories(self):
        # Log in successfully
        self.login("user1", "user123")

        # Navigate to the Bookmarks Page
        self.driver.get('http://localhost:8309/bookmarks')

        # Verify that the list of bookmarked stories is displayed correctly
        self.assertIn("Story Title 1", self.driver.page_source)

    def test_user_logout(self):
        # Log in successfully
        self.login("user1", "user123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8309/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
