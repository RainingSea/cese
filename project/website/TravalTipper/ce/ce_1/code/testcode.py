import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelTipperApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8435/')  # Use the port specified in main.py

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8435/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8435/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify error message for existing username
        self.assertIn("Registration failed", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Travel Tips", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8435/')
        self.login("invalid_user", "invalid_password")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_input_travel_details(self):
        # Functionality 3: Input Travel Details
        self.login("admin", "admin123")  # Login first
        self.assertIn("Travel Tips", self.driver.title)

        # Input valid travel details
        self.driver.find_element(By.NAME, 'destination').send_keys("Paris")
        self.driver.find_element(By.NAME, 'interests').click()  # Select an interest
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify tips are generated
        self.assertIn("Visit the Eiffel Tower", self.driver.page_source)

        # Attempt to submit with incomplete details
        self.driver.find_element(By.NAME, 'destination').clear()
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        self.assertIn("This field is required", self.driver.page_source)

    def test_view_recommendations(self):
        # Functionality 4: View Recommendations
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'destination').send_keys("New York")
        self.driver.find_element(By.NAME, 'interests').click()
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify recommendations are displayed
        self.assertIn("Explore Central Park", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

        # Attempt to access the main page after logout
        self.driver.get('http://localhost:8435/main')
        self.assertIn("Invalid credentials", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
