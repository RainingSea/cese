import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestTravelRecommenderApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8560/')

    def tearDown(self):
        # Close the web driver session and stop the web application
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

        # Register a new user
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
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify an error message is displayed
        self.assertIn("Username already exists", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("admin", "admin123")

        # Verify redirection to the preferences page
        self.assertIn("Preferences", self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8560/')
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Invalid username or password", self.driver.page_source)

    def test_input_travel_preferences(self):
        # Login and navigate to preferences page
        self.login("admin", "admin123")
        self.assertIn("Preferences", self.driver.title)

        # Fill in travel preferences
        self.driver.find_element(By.NAME, 'budget').send_keys('1000')
        self.driver.find_element(By.NAME, 'activities').send_keys('beach')
        self.driver.find_element(By.NAME, 'climate').send_keys('tropical')
        self.driver.find_element(By.XPATH, '//button[text()="Submit Preferences"]').click()
        time.sleep(1)

        # Verify redirection to recommendations page
        self.assertIn("Recommendations", self.driver.title)

    def test_generate_travel_recommendations(self):
        # Login and input preferences
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'budget').send_keys('1000')
        self.driver.find_element(By.NAME, 'activities').send_keys('beach')
        self.driver.find_element(By.NAME, 'climate').send_keys('tropical')
        self.driver.find_element(By.XPATH, '//button[text()="Submit Preferences"]').click()
        time.sleep(1)

        # Verify recommendations are displayed
        destinations = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(destinations), 0, "No recommendations found.")

        # Check details of a recommended destination
        destinations[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)
        self.assertIn("Activities", self.driver.page_source)

    def test_save_favorite_destinations(self):
        # Login and navigate to recommendations
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'budget').send_keys('1000')
        self.driver.find_element(By.NAME, 'activities').send_keys('beach')
        self.driver.find_element(By.NAME, 'climate').send_keys('tropical')
        self.driver.find_element(By.XPATH, '//button[text()="Submit Preferences"]').click()
        time.sleep(1)

        # Save a destination to favorites
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        time.sleep(1)

        # Navigate to favorites
        self.driver.find_element(By.LINK_TEXT, 'Favorites').click()
        time.sleep(1)

        # Verify the destination is in favorites
        self.assertIn("Bali", self.driver.page_source)

    def test_user_logout(self):
        # Login and logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to access preferences page
        self.driver.get('http://localhost:8560/preferences')
        self.assertIn("Login", self.driver.title)

    def test_view_detailed_information_about_destinations(self):
        # Login and navigate to recommendations
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'budget').send_keys('1000')
        self.driver.find_element(By.NAME, 'activities').send_keys('beach')
        self.driver.find_element(By.NAME, 'climate').send_keys('tropical')
        self.driver.find_element(By.XPATH, '//button[text()="Submit Preferences"]').click()
        time.sleep(1)

        # View details of a destination
        self.driver.find_element(By.LINK_TEXT, 'Bali').click()
        time.sleep(1)

        # Verify detailed information is displayed
        self.assertIn("Activities", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
