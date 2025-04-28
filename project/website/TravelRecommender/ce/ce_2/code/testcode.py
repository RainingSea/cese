import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelRecommenderApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8444/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8444/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "testuser"
        new_password = "testpass"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8444/register')  # Navigate to Registration Page
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Check for error message
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Travel Preferences", self.driver.title)  # Check redirection to preferences page

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8444/')  # Navigate to Login Page
        self.login("admin", "wrongpassword")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_input_travel_preferences(self):
        # Functionality 3: Input Travel Preferences
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8444/preferences')  # Navigate to preferences page
        self.assertIn("Travel Preferences", self.driver.title)

        # Fill in preferences
        self.driver.find_element(By.NAME, 'budget').send_keys("2000")
        self.driver.find_element(By.NAME, 'activities').send_keys("sightseeing")
        self.driver.find_element(By.NAME, 'climate').send_keys("warm")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Preferences"]').click()

        # Verify redirection to recommendations page
        self.assertIn("Your Travel Recommendations", self.driver.title)

    def test_generate_travel_recommendations(self):
        # Functionality 4: Generate Travel Recommendations
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8444/preferences')  # Navigate to preferences page

        # Fill in preferences
        self.driver.find_element(By.NAME, 'budget').send_keys("2000")
        self.driver.find_element(By.NAME, 'activities').send_keys("sightseeing")
        self.driver.find_element(By.NAME, 'climate').send_keys("warm")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Preferences"]').click()

        # Check recommendations
        self.assertIn("Paris", self.driver.page_source)  # Check if Paris is in recommendations

    def test_view_destination_details(self):
        # Functionality 7: View Detailed Information About Destinations
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8444/preferences')  # Navigate to preferences page

        # Fill in preferences
        self.driver.find_element(By.NAME, 'budget').send_keys("2000")
        self.driver.find_element(By.NAME, 'activities').send_keys("sightseeing")
        self.driver.find_element(By.NAME, 'climate').send_keys("warm")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Preferences"]').click()

        # Click on destination details
        self.driver.find_element(By.LINK_TEXT, 'Details for Paris').click()  # Assuming link text is as such
        self.assertIn("Details for Paris", self.driver.title)  # Check if details page is displayed

if __name__ == '__main__':
    unittest.main()
