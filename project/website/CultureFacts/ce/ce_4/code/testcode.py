import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestCultureFactsApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:9020/')

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
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that an error message is displayed
        self.assertIn("Registration failed. Username already exists.", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:9020/')
        self.login("invalid_user", "invalid_pass")

        # Verify that an error message is displayed
        self.assertIn("Login failed. Check your username and password.", self.driver.page_source)

    def test_explore_cultures_on_dashboard(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify that a list of available cultures is displayed
        cultures = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cultures), 0, "No cultures found on the Dashboard.")

        # Click on a culture from the list
        cultures[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Culture Details Page
        self.assertIn("Details about", self.driver.page_source)

    def test_view_culture_details(self):
        # Navigate to the Dashboard Page and select a culture
        self.login("admin", "admin123")
        self.driver.find_elements(By.TAG_NAME, 'li')[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Culture Details Page is displayed with detailed information
        self.assertIn("Details about", self.driver.page_source)

    def test_search_for_cultures_or_facts(self):
        # This functionality is not implemented in the codebase
        self.fail("Search functionality not implemented")

    def test_bookmark_culture_facts(self):
        # Navigate to the Culture Details Page for a specific culture
        self.login("admin", "admin123")
        self.driver.find_elements(By.TAG_NAME, 'li')[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)  # Wait for the next page to load

        # Click the "Bookmark" button
        self.driver.find_element(By.XPATH, '//button[text()="Bookmark"]').click()
        time.sleep(1)  # Wait for the action to complete

        # Verify that the culture fact is added to the user's bookmarks
        self.driver.find_element(By.LINK_TEXT, 'View Bookmarks').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Culture A", self.driver.page_source)

    def test_view_and_manage_bookmarks(self):
        # This functionality is not fully implemented in the codebase
        self.fail("Manage bookmarks functionality not implemented")

    def test_user_logout(self):
        # Logout from the Dashboard Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:9020/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # This functionality is not implemented in the codebase
        self.fail("Local data storage functionality not implemented")

if __name__ == '__main__':
    unittest.main()
