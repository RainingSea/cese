import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelRecommenderApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8673/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()

        # Verify user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()

        # Expectation: An error message is displayed indicating that the username is already taken
        self.assertIn("Register", self.driver.title)  # Assuming it stays on the same page

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Expectation: Access is granted, and the user is redirected to the Dashboard Page
        self.assertNotIn("Login", self.driver.title)  # Assuming redirection happens

        # Enter an invalid username or password
        self.driver.get('http://localhost:8673/')  # Navigate back to login
        self.login("invalid_user", "wrong_password")

        # Expectation: An error message is displayed indicating invalid credentials
        self.assertIn("Login", self.driver.title)  # Assuming it stays on the login page

    def test_input_travel_preferences(self):
        # Login successfully
        self.login("admin", "admin123")

        # Navigate to the preferences input page
        self.driver.get('http://localhost:8673/preferences')

        # Verify the preferences input form is displayed
        self.assertIn("Preferences", self.driver.title)

        # Fill in the travel preferences and submit the form
        self.driver.find_element(By.NAME, 'budget').send_keys("1500")
        self.driver.find_element(By.XPATH, '//input[@value="Sightseeing"]').click()
        self.driver.find_element(By.NAME, 'climate').send_keys("Warm")
        self.driver.find_element(By.XPATH, '//input[@value="Save Preferences"]').click()

        # Expectation: The preferences are saved successfully, and the user is redirected to the recommendations page
        self.assertIn("Recommendations", self.driver.title)

    def test_generate_travel_recommendations(self):
        # Login and input preferences
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8673/preferences')
        self.driver.find_element(By.NAME, 'budget').send_keys("1500")
        self.driver.find_element(By.XPATH, '//input[@value="Sightseeing"]').click()
        self.driver.find_element(By.NAME, 'climate').send_keys("Warm")
        self.driver.find_element(By.XPATH, '//input[@value="Save Preferences"]').click()

        # Expectation: A list of personalized travel destinations is displayed
        self.assertIn("Recommendations", self.driver.title)

        # Check the details of a recommended destination
        destinations = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(destinations), 0, "No destinations found.")

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
