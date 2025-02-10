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
        self.driver.get('http://localhost:8674/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and terminate the app process
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
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify the user is redirected to the preferences page
        self.assertIn("Preferences", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8674/')
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)

    def test_input_travel_preferences(self):
        # Login successfully
        self.login("admin", "admin123")

        # Verify the preferences input form is displayed
        self.assertIn("Preferences", self.driver.title)

        # Fill in the travel preferences and submit the form
        self.driver.find_element(By.NAME, 'budget').send_keys("2000")
        self.driver.find_element(By.XPATH, '//input[@value="Hiking"]').click()
        self.driver.find_element(By.XPATH, '//input[@value="Cultural"]').click()
        self.driver.find_element(By.NAME, 'climate').send_keys("Temperate")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Preferences"]').click()
        time.sleep(1)

        # Verify the user is redirected to the recommendations page
        self.assertIn("Recommendations", self.driver.title)

    def test_generate_travel_recommendations(self):
        # Login and input preferences
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'budget').send_keys("2000")
        self.driver.find_element(By.XPATH, '//input[@value="Hiking"]').click()
        self.driver.find_element(By.XPATH, '//input[@value="Cultural"]').click()
        self.driver.find_element(By.NAME, 'climate').send_keys("Temperate")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Preferences"]').click()
        time.sleep(1)

        # Verify a list of recommendations is displayed
        recommendations = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(recommendations), 0, "No recommendations found.")

        # Check the details of a recommended destination
        recommendations[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)

        # Verify detailed information is displayed
        self.assertIn("Destination Details", self.driver.title)

    def test_save_favorite_destinations(self):
        # This functionality is not implemented in the codebase
        self.fail("Save favorite destinations functionality not implemented")

    def test_user_logout(self):
        # Login successfully
        self.login("admin", "admin123")

        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the preferences page after logging out
        self.driver.get('http://localhost:8674/preferences')
        self.assertIn("Login", self.driver.title)

    def test_view_detailed_information_about_destinations(self):
        # Login and input preferences
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'budget').send_keys("2000")
        self.driver.find_element(By.XPATH, '//input[@value="Hiking"]').click()
        self.driver.find_element(By.XPATH, '//input[@value="Cultural"]').click()
        self.driver.find_element(By.NAME, 'climate').send_keys("Temperate")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Preferences"]').click()
        time.sleep(1)

        # Click on a recommended destination
        recommendations = self.driver.find_elements(By.TAG_NAME, 'li')
        recommendations[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)

        # Verify detailed information is displayed
        self.assertIn("Destination Details", self.driver.title)

        # Check details for multiple destinations
        self.driver.get('http://localhost:8674/recommendations')
        recommendations = self.driver.find_elements(By.TAG_NAME, 'li')
        recommendations[1].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)
        self.assertIn("Destination Details", self.driver.title)

if __name__ == '__main__':
    unittest.main()
