import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestCultureFactsApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:9019/')  # Navigate to the login page

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

        # Verify the Registration Page is displayed
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
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("user1")
        self.driver.find_element(By.NAME, 'password').send_keys("user123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)  # Assuming it stays on the registration page

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("user1", "user123")

        # Verify access is granted and redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:9019/')  # Navigate back to login
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)  # Assuming it stays on the login page

    def test_explore_cultures_on_dashboard(self):
        # Login and navigate to the Dashboard Page
        self.login("user1", "user123")

        # Verify a list of available cultures is displayed
        cultures = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(cultures), 0, "No cultures found on the dashboard.")

        # Click on a culture from the list
        cultures[0].click()
        time.sleep(1)

        # Verify redirection to the Culture Details Page
        self.assertIn("Culture Details", self.driver.title)

    def test_view_culture_details(self):
        # Login and navigate to the Dashboard Page
        self.login("user1", "user123")

        # Select a culture
        self.driver.find_elements(By.TAG_NAME, 'li')[0].click()
        time.sleep(1)

        # Verify the Culture Details Page is displayed with detailed information
        self.assertIn("Culture Details", self.driver.title)
        self.assertIn("Rich in traditions", self.driver.page_source)

    def test_search_for_cultures_or_facts(self):
        # This functionality is not implemented in the codebase
        self.fail("Search functionality not implemented")

    def test_bookmark_culture_facts(self):
        # Login and navigate to the Dashboard Page
        self.login("user1", "user123")

        # Navigate to the Culture Details Page for a specific culture
        self.driver.find_elements(By.TAG_NAME, 'li')[0].click()
        time.sleep(1)

        # Click the "Bookmark" button
        self.driver.find_element(By.XPATH, '//button[text()="Bookmark"]').click()
        time.sleep(1)

        # Verify the culture fact is added to the user's bookmarks
        self.driver.find_element(By.LINK_TEXT, 'My Bookmarks').click()
        time.sleep(1)
        self.assertIn("Japanese", self.driver.page_source)

    def test_view_and_manage_bookmarks(self):
        # This functionality is not implemented in the codebase
        self.fail("Manage bookmarks functionality not implemented")

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("user1", "user123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:9019/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # This functionality is not implemented in the codebase
        self.fail("Local data storage functionality not implemented")

if __name__ == '__main__':
    unittest.main()
