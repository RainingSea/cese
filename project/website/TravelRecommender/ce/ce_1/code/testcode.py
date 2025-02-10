import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTravelRecommenderApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8672/')  # Navigate to the login page

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

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the error message

        # Verify an error message is displayed
        self.assertIn("username is already taken", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify the user is redirected to the Dashboard Page
        self.assertNotIn("Login", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8672/')  # Navigate back to the login page
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("invalid credentials", self.driver.page_source)

    def test_input_travel_preferences(self):
        # Login successfully
        self.login("admin", "admin123")

        # Navigate to the preferences input page
        self.driver.get('http://localhost:8672/preferences')
        time.sleep(1)  # Wait for the page to load

        # Verify the preferences input form is displayed
        self.assertIn("Travel Preferences", self.driver.title)

        # Fill in the travel preferences and submit the form
        self.driver.find_element(By.NAME, 'budget').send_keys("1000")
        self.driver.find_element(By.NAME, 'activities').click()  # Select hiking
        self.driver.find_element(By.NAME, 'climate').send_keys("temperate")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Preferences"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the recommendations page
        self.assertIn("Recommendations", self.driver.title)

    def test_generate_travel_recommendations(self):
        # Login and input travel preferences
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8672/preferences')
        self.driver.find_element(By.NAME, 'budget').send_keys("1000")
        self.driver.find_element(By.NAME, 'activities').click()  # Select hiking
        self.driver.find_element(By.NAME, 'climate').send_keys("temperate")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Preferences"]').click()
        time.sleep(1)  # Wait for the recommendations page

        # Verify a list of personalized travel destinations is displayed
        recommendations = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(recommendations), 0, "No recommendations found.")

        # Check the details of a recommended destination
        self.assertIn("Hawaii", self.driver.page_source)

    def test_save_favorite_destinations(self):
        # This functionality is not implemented in the codebase
        self.fail("Save Favorite Destinations functionality is not implemented")

    def test_user_logout(self):
        # Login successfully
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8672/preferences')
        self.assertIn("Login", self.driver.title)

    def test_view_detailed_information_about_destinations(self):
        # This functionality is not implemented in the codebase
        self.fail("View Detailed Information About Destinations functionality is not implemented")

if __name__ == '__main__':
    unittest.main()
