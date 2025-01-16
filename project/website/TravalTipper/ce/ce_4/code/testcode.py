import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTravelTipperApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8663/')  # Navigate to the login page

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
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register here.").click()
        time.sleep(1)

        # Enter a valid username and password
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify successful registration
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register here.").click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys('user1')
        self.driver.find_element(By.NAME, 'password').send_keys('user123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Check for error message (not implemented in the codebase)
        self.fail("Error message for existing username not implemented")

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8663/')
        time.sleep(1)

        # Enter valid credentials
        self.login('user1', 'user123')

        # Verify redirection to the Dashboard Page
        self.assertIn("Travel Details", self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8663/')
        self.login('invalid_user', 'wrong_password')

        # Check for error message (not implemented in the codebase)
        self.fail("Error message for invalid login not implemented")

    def test_input_travel_details(self):
        # Login and navigate to Travel Tips input section
        self.login('user1', 'user123')

        # Verify Travel Tips input form is displayed
        self.assertIn("Travel Details", self.driver.title)

        # Enter valid travel details
        self.driver.find_element(By.NAME, 'destination').send_keys('Paris')
        self.driver.find_element(By.NAME, 'duration').send_keys('5 days')
        self.driver.find_element(By.NAME, 'interests').send_keys('art,food')
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()
        time.sleep(1)

        # Verify recommendations are displayed
        self.assertIn("Recommendations for Paris", self.driver.page_source)

        # Submit incomplete travel details
        self.driver.get('http://localhost:8663/travel_details')
        self.driver.find_element(By.NAME, 'destination').send_keys('')
        self.driver.find_element(By.NAME, 'duration').send_keys('')
        self.driver.find_element(By.NAME, 'interests').send_keys('')
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()
        time.sleep(1)

        # Check for error message (not implemented in the codebase)
        self.fail("Error message for incomplete travel details not implemented")

    def test_view_recommendations(self):
        # Login and input travel details
        self.login('user1', 'user123')
        self.driver.find_element(By.NAME, 'destination').send_keys('Paris')
        self.driver.find_element(By.NAME, 'duration').send_keys('5 days')
        self.driver.find_element(By.NAME, 'interests').send_keys('art,food')
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()
        time.sleep(1)

        # Verify recommendations are displayed
        self.assertIn("Recommendations for Paris", self.driver.page_source)

        # Refresh the page and verify recommendations remain
        self.driver.refresh()
        time.sleep(1)
        self.assertIn("Recommendations for Paris", self.driver.page_source)

    def test_search_for_tips(self):
        # This functionality is not implemented in the codebase
        self.fail("Search for tips functionality not implemented")

    def test_save_favorite_travel_tips(self):
        # Login and input travel details
        self.login('user1', 'user123')
        self.driver.find_element(By.NAME, 'destination').send_keys('Paris')
        self.driver.find_element(By.NAME, 'duration').send_keys('5 days')
        self.driver.find_element(By.NAME, 'interests').send_keys('art,food')
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()
        time.sleep(1)

        # Save a favorite tip
        self.driver.find_element(By.NAME, 'tip').send_keys('Visit the Louvre and enjoy local cuisine.')
        self.driver.find_element(By.XPATH, '//button[text()="Save Favorite"]').click()
        time.sleep(1)

        # Verify the tip is saved
        self.driver.find_element(By.LINK_TEXT, 'View Favorites').click()
        time.sleep(1)
        self.assertIn("Visit the Louvre and enjoy local cuisine.", self.driver.page_source)

        # Attempt to save the same tip again (not implemented in the codebase)
        self.fail("Duplicate favorite tip saving not implemented")

    def test_user_logout(self):
        # Login and logout
        self.login('user1', 'user123')
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logout
        self.driver.get('http://localhost:8663/travel_details')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Login and input travel details
        self.login('user1', 'user123')
        self.driver.find_element(By.NAME, 'destination').send_keys('Paris')
        self.driver.find_element(By.NAME, 'duration').send_keys('5 days')
        self.driver.find_element(By.NAME, 'interests').send_keys('art,food')
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()
        time.sleep(1)

        # Navigate back to the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Back to Travel Details').click()
        time.sleep(1)

        # Verify redirection to the Dashboard Page
        self.assertIn("Travel Details", self.driver.title)

    def test_view_saved_travel_tips(self):
        # Login and navigate to favorites
        self.login('user1', 'user123')
        self.driver.find_element(By.LINK_TEXT, 'View Favorites').click()
        time.sleep(1)

        # Verify saved travel tips are displayed
        self.assertIn("Visit the Louvre and enjoy local cuisine.", self.driver.page_source)

        # Click on a saved travel tip to view details (not implemented in the codebase)
        self.fail("Viewing details of a saved travel tip not implemented")

if __name__ == '__main__':
    unittest.main()
