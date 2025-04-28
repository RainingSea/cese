import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelTipperApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8434/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the app process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8434/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8434/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Check for error message
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8434/')
        self.login("invalid_user", "wrong_password")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_input_travel_details(self):
        # Functionality 3: Input Travel Details
        self.login("admin", "admin123")  # Login first
        self.driver.get('http://localhost:8434/travel_details')  # Navigate to Travel Tips input section
        self.assertIn("Travel Details", self.driver.title)

        # Submit valid travel details
        self.driver.find_element(By.NAME, 'destination').send_keys("Paris")
        self.driver.find_element(By.NAME, 'duration').send_keys("5 days")
        self.driver.find_element(By.NAME, 'interests').send_keys("sightseeing")
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()

        # Verify that tips are displayed
        self.assertIn("Travel Tips", self.driver.page_source)

        # Submit incomplete travel details
        self.driver.find_element(By.NAME, 'destination').clear()  # Clear destination
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()
        self.assertIn("All fields are required", self.driver.page_source)

    def test_view_recommendations(self):
        # Functionality 4: View Recommendations
        self.login("admin", "admin123")  # Login first
        self.driver.get('http://localhost:8434/travel_details')
        self.driver.find_element(By.NAME, 'destination').send_keys("Paris")
        self.driver.find_element(By.NAME, 'duration').send_keys("5 days")
        self.driver.find_element(By.NAME, 'interests').send_keys("sightseeing")
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()

        # Verify recommendations are displayed
        self.assertIn("Travel Tips", self.driver.page_source)

        # Refresh the page and check if recommendations remain visible
        self.driver.refresh()
        self.assertIn("Travel Tips", self.driver.page_source)

    def test_save_favorite_travel_tips(self):
        # Functionality 6: Save Favorite Travel Tips
        self.login("admin", "admin123")  # Login first
        self.driver.get('http://localhost:8434/travel_details')
        self.driver.find_element(By.NAME, 'destination').send_keys("Paris")
        self.driver.find_element(By.NAME, 'duration').send_keys("5 days")
        self.driver.find_element(By.NAME, 'interests').send_keys("sightseeing")
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()

        # Assume there's a save button next to the tips
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()  # Save a tip
        self.assertIn("Tip saved to favorites", self.driver.page_source)

        # Check favorites
        self.driver.get('http://localhost:8434/favorites')
        self.assertIn("Paris", self.driver.page_source)  # Check if the saved tip is present

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Login first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 8: Navigate Back to Dashboard
        self.login("admin", "admin123")  # Login first
        self.driver.get('http://localhost:8434/travel_details')
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        self.assertIn("Dashboard", self.driver.title)

    def test_view_saved_travel_tips(self):
        # Functionality 9: View Saved Travel Tips
        self.login("admin", "admin123")  # Login first
        self.driver.get('http://localhost:8434/favorites')
        self.assertIn("Your Saved Tips", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
