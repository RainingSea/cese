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
        self.driver.get('http://localhost:8671/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, "Register here").click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, "Register here").click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed (assuming the application shows an error)
        self.assertIn("Register", self.driver.title)  # Still on the registration page

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and the user is redirected to the Dashboard Page
        self.assertIn("Recommendations", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8671/')  # Navigate back to the login page
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed (assuming the application shows an error)
        self.assertIn("Login", self.driver.title)  # Still on the login page

    def test_input_travel_preferences(self):
        # Login successfully
        self.login("admin", "admin123")

        # Verify the preferences input form is displayed
        self.assertIn("Recommendations", self.driver.title)

        # Fill in the travel preferences and submit the form
        self.driver.find_element(By.NAME, 'budget').send_keys("1000")
        self.driver.find_element(By.NAME, 'activities').send_keys("sightseeing")
        self.driver.find_element(By.NAME, 'climate').send_keys("temperate")
        self.driver.find_element(By.XPATH, '//input[@value="Get Recommendations"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the recommendations page
        self.assertIn("Recommendations", self.driver.title)

    def test_generate_travel_recommendations(self):
        # Login and input travel preferences
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'budget').send_keys("1000")
        self.driver.find_element(By.NAME, 'activities').send_keys("sightseeing")
        self.driver.find_element(By.NAME, 'climate').send_keys("temperate")
        self.driver.find_element(By.XPATH, '//input[@value="Get Recommendations"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify a list of personalized travel destinations is displayed
        recommendations = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(recommendations), 0, "No recommendations found.")

        # Check the details of a recommended destination
        destination_details = recommendations[0].text
        self.assertIn("Activities", destination_details)
        self.assertIn("Climate", destination_details)
        self.assertIn("Cost", destination_details)

    def test_save_favorite_destinations(self):
        # This functionality is not implemented in the codebase
        self.fail("Save favorite destinations functionality not implemented")

    def test_user_logout(self):
        # This functionality is not implemented in the codebase
        self.fail("User logout functionality not implemented")

    def test_view_detailed_information_about_destinations(self):
        # This functionality is not implemented in the codebase
        self.fail("View detailed information about destinations functionality not implemented")

if __name__ == '__main__':
    unittest.main()
