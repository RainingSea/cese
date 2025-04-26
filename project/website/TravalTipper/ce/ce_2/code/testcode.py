import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelTipperApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8264/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8264/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8264/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Expectation: Error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Travel Details", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8264/')
        self.login("admin", "wrong_password")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_input_travel_details(self):
        # Functionality 3: Input Travel Details
        self.login("admin", "admin123")  # Login first
        self.driver.get('http://localhost:8264/travel_details')  # Navigate to Travel Details

        # Verify the form is displayed
        self.assertIn("Travel Details", self.driver.title)

        # Submit valid travel details
        self.driver.find_element(By.NAME, 'destination').send_keys("Paris")
        self.driver.find_element(By.NAME, 'duration').send_keys("5 days")
        self.driver.find_element(By.NAME, 'interests').click()  # Select an interest
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()

        # Verify recommendations are displayed
        self.assertIn("Personalized Travel Tips", self.driver.page_source)

        # Attempt to submit incomplete details
        self.driver.get('http://localhost:8264/travel_details')
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()
        self.assertIn("All fields are required", self.driver.page_source)

    def test_view_recommendations(self):
        # Functionality 4: View Recommendations
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8264/travel_details')
        self.driver.find_element(By.NAME, 'destination').send_keys("Tokyo")
        self.driver.find_element(By.NAME, 'duration').send_keys("3 days")
        self.driver.find_element(By.NAME, 'interests').click()
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()

        # Verify recommendations are displayed
        self.assertIn("Personalized Travel Tips", self.driver.page_source)

    def test_save_favorite_tips(self):
        # Functionality 6: Save Favorite Travel Tips
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8264/travel_details')
        self.driver.find_element(By.NAME, 'destination').send_keys("New York")
        self.driver.find_element(By.NAME, 'duration').send_keys("4 days")
        self.driver.find_element(By.NAME, 'interests').click()
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()

        # Simulate saving a favorite tip
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()  # Assuming a save button exists
        self.assertIn("Tip saved to favorites", self.driver.page_source)

        # Navigate to favorites
        self.driver.get('http://localhost:8264/favorites')
        self.assertIn("Your Favorite Tips", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
