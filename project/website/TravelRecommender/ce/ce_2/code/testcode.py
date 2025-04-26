import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelRecommenderApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8272/')  # Access the login page

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
        self.driver.get('http://localhost:8272/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8272/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message
        self.assertIn("Registration failed", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Preferences", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8272/')
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Login failed", self.driver.page_source)

    def test_input_travel_preferences(self):
        # Functionality 3: Input Travel Preferences
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8272/preferences')  # Navigate to preferences page
        self.assertIn("Travel Preferences", self.driver.title)

        # Fill in travel preferences
        self.driver.find_element(By.NAME, 'budget').send_keys("600")
        self.driver.find_element(By.NAME, 'activities').click()  # Select hiking
        self.driver.find_element(By.NAME, 'activities').click()  # Select beach
        self.driver.find_element(By.NAME, 'climate').send_keys("tropical")
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()

        # Verify redirection to recommendations page
        self.assertIn("Your Travel Recommendations", self.driver.title)

    def test_generate_travel_recommendations(self):
        # Functionality 4: Generate Travel Recommendations
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8272/preferences')  # Navigate to preferences page

        # Fill in travel preferences
        self.driver.find_element(By.NAME, 'budget').send_keys("600")
        self.driver.find_element(By.NAME, 'activities').click()  # Select hiking
        self.driver.find_element(By.NAME, 'climate').send_keys("tropical")
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()

        # Verify recommendations are displayed
        self.assertIn("Bali", self.driver.page_source)  # Check for a specific recommendation

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8272/preferences')  # Navigate to preferences page

        # Click the Logout button (assumed to be present)
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)  # Verify redirection to login page

if __name__ == '__main__':
    unittest.main()
