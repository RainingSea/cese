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
        self.driver.get('http://localhost:8659/')

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

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check for error message
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")
        self.assertIn("Travel Details", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8659/')
        self.login("invalid_user", "invalid_pass")
        self.assertIn("Login", self.driver.title)

    def test_input_travel_details(self):
        # Login successfully and navigate to the Travel Tips input section
        self.login("admin", "admin123")
        self.assertIn("Travel Details", self.driver.title)

        # Enter valid travel details and submit
        self.driver.find_element(By.NAME, 'destination').send_keys('Paris')
        self.driver.find_element(By.NAME, 'trip_duration').send_keys('3 days')
        self.driver.find_element(By.XPATH, '//option[@value="culture"]').click()
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Submit the form with incomplete travel details
        self.driver.get('http://localhost:8659/travel_details')
        self.driver.find_element(By.NAME, 'destination').send_keys('')
        self.driver.find_element(By.NAME, 'trip_duration').send_keys('')
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check for error message
        self.assertIn("Travel Details", self.driver.title)

    def test_view_recommendations(self):
        # Login and input travel details
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'destination').send_keys('Paris')
        self.driver.find_element(By.NAME, 'trip_duration').send_keys('3 days')
        self.driver.find_element(By.XPATH, '//option[@value="culture"]').click()
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify recommendations are displayed
        self.assertIn("Recommendations", self.driver.title)

        # Refresh the page and verify recommendations remain
        self.driver.refresh()
        self.assertIn("Recommendations", self.driver.title)

    def test_search_for_tips(self):
        # Not implemented in the codebase
        self.fail("Search functionality not implemented")

    def test_save_favorite_travel_tips(self):
        # Not implemented in the codebase
        self.fail("Save favorite travel tips functionality not implemented")

    def test_user_logout(self):
        # Login and then logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8659/travel_details')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Login and input travel details
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'destination').send_keys('Paris')
        self.driver.find_element(By.NAME, 'trip_duration').send_keys('3 days')
        self.driver.find_element(By.XPATH, '//option[@value="culture"]').click()
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Click back to return to the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Input Travel Details').click()
        self.assertIn("Travel Details", self.driver.title)

    def test_view_saved_travel_tips(self):
        # Not implemented in the codebase
        self.fail("View saved travel tips functionality not implemented")

if __name__ == '__main__':
    unittest.main()
