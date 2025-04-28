import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestTravelRecommenderApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8443/') 

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

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8443/register')
        self.assertIn("Register", self.driver.title)

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8443/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for existing username
        self.assertIn("Username already exists!", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8443/')
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Recommendations", self.driver.title)

        # Invalid login
        self.driver.get('http://localhost:8443/')
        self.login("admin", "wrongpassword")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_input_travel_preferences(self):
        # Functionality 3: Input Travel Preferences
        self.login("user1", "user123")
        self.driver.get('http://localhost:8443/preferences')
        self.assertIn("Travel Preferences", self.driver.title)

        # Fill in travel preferences
        self.driver.find_element(By.NAME, 'destination').send_keys("Beach")
        self.driver.find_element(By.NAME, 'travel_type').send_keys("Leisure")
        self.driver.find_element(By.XPATH, '//button[text()="Save Preferences"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to recommendations page
        self.assertIn("Your Travel Recommendations", self.driver.title)

    def test_generate_travel_recommendations(self):
        # Functionality 4: Generate Travel Recommendations
        self.login("user1", "user123")
        self.driver.get('http://localhost:8443/recommendations')
        self.assertIn("Your Travel Recommendations", self.driver.title)

        # Check if recommendations are displayed
        recommendations = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(recommendations), 0, "No recommendations found.")

    def test_save_favorite_destinations(self):
        # Functionality 5: Save Favorite Destinations
        self.login("user1", "user123")
        self.driver.get('http://localhost:8443/recommendations')
        self.assertIn("Your Travel Recommendations", self.driver.title)

        # Attempt to save a favorite (assuming a save button exists next to each recommendation)
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()  # Adjust selector as needed
        time.sleep(1)  # Wait for the action to complete

        # Verify that the destination is saved (this would require checking the favorites page)
        self.driver.get('http://localhost:8443/favorites')
        self.assertIn("Your Favorite Destinations", self.driver.title)

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_view_detailed_information(self):
        # Functionality 7: View Detailed Information About Destinations
        self.login("user1", "user123")
        self.driver.get('http://localhost:8443/recommendations')
        self.assertIn("Your Travel Recommendations", self.driver.title)

        # Click on a destination (assuming each destination is a link)
        self.driver.find_element(By.XPATH, '//li[1]').click()  # Adjust selector as needed
        time.sleep(1)  # Wait for the next page to load

        # Verify that detailed information is displayed
        self.assertIn("Detailed Information", self.driver.title)  # Adjust based on actual title

if __name__ == '__main__':
    unittest.main()
