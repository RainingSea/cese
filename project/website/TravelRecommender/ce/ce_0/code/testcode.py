import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelRecommenderApp(unittest.TestCase):

    def setUp(self):
        # Start the server and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8080/') 

    def tearDown(self):
        # Close the web driver session and terminate the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8080/register')
        
        # Verify Registration Page is displayed
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
        self.driver.get('http://localhost:8080/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify error message for existing username
        self.assertIn("400", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify that the user is redirected to the preferences page
        self.assertIn("Travel Preferences", self.driver.title)

        # Test invalid login
        self.driver.get('http://localhost:8080/')
        self.login("invalid_user", "invalid_password")

        # Verify error message for invalid credentials
        self.assertIn("401", self.driver.page_source)

    def test_input_travel_preferences(self):
        # Functionality 3: Input Travel Preferences
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8080/preferences')

        # Verify preferences input form is displayed
        self.assertIn("Travel Preferences", self.driver.title)

        # Fill in travel preferences
        self.driver.find_element(By.NAME, 'budget').send_keys("1500")
        self.driver.find_element(By.NAME, 'activities').click()  # Select an activity
        self.driver.find_element(By.NAME, 'climate').send_keys("Tropical")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify redirection to recommendations page
        self.assertIn("Recommendations", self.driver.title)

    def test_generate_travel_recommendations(self):
        # Functionality 4: Generate Travel Recommendations
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8080/preferences')

        # Fill in travel preferences
        self.driver.find_element(By.NAME, 'budget').send_keys("1500")
        self.driver.find_element(By.NAME, 'activities').click()  # Select an activity
        self.driver.find_element(By.NAME, 'climate').send_keys("Tropical")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify recommendations are displayed
        self.assertIn("Recommended Destinations", self.driver.page_source)

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8080/preferences')

        # Simulate logout (assuming there's a logout button)
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to access preferences page after logout
        self.driver.get('http://localhost:8080/preferences')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
