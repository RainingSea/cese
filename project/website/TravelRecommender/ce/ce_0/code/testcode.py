import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelRecommenderApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8442/') 

    def tearDown(self):
        # Close the web driver session and terminate the subprocess
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8442/register')
        
        # Verify that the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8442/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already exists!", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify that the user is redirected to the preferences page
        self.assertIn("Travel Preferences", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8442/')
        self.login("admin", "wrongpassword")  # Invalid password

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_input_travel_preferences(self):
        # Functionality 3: Input Travel Preferences
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8442/preferences')

        # Verify that the preferences input form is displayed
        self.assertIn("Travel Preferences", self.driver.title)

        # Fill in the travel preferences and submit the form
        self.driver.find_element(By.NAME, 'budget').send_keys("1000")
        self.driver.find_element(By.NAME, 'activities').send_keys("Sightseeing")
        self.driver.find_element(By.NAME, 'climate').send_keys("Temperate")
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()

        # Verify that the recommendations page is displayed
        self.assertIn("Your Recommendations", self.driver.title)

    def test_generate_travel_recommendations(self):
        # Functionality 4: Generate Travel Recommendations
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8442/preferences')

        # Fill in the travel preferences and submit the form
        self.driver.find_element(By.NAME, 'budget').send_keys("1000")
        self.driver.find_element(By.NAME, 'activities').send_keys("Sightseeing")
        self.driver.find_element(By.NAME, 'climate').send_keys("Temperate")
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()

        # Verify that recommendations are displayed
        recommendations = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(recommendations), 0, "No recommendations found.")

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
