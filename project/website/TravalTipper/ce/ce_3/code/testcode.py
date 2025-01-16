import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTravelTipperApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8662/login')

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

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.get('http://localhost:8662/register')
        self.assertIn("Registration", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Check for registration success message
        self.assertIn("Registration successful! Please log in.", self.driver.page_source)

        # Attempt to register with an existing username
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Check for error message
        self.assertIn("Username already exists. Please choose a different one.", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8662/login')
        self.assertIn("Login", self.driver.title)

        # Login with valid credentials
        self.login("admin", "admin123")
        self.assertIn("Travel Tips", self.driver.title)

        # Login with invalid credentials
        self.driver.get('http://localhost:8662/login')
        self.login("invalid_user", "invalid_pass")
        self.assertIn("Invalid username or password. Please try again.", self.driver.page_source)

    def test_input_travel_details(self):
        # Login and navigate to Travel Tips page
        self.login("admin", "admin123")
        self.assertIn("Travel Tips", self.driver.title)

        # Enter valid travel details
        self.driver.find_element(By.NAME, 'destination').send_keys("Paris")
        self.driver.find_element(By.NAME, 'tips').send_keys("Visit the Eiffel Tower")
        self.driver.find_element(By.XPATH, '//button[text()="Add Tip"]').click()
        time.sleep(1)

        # Check for success message
        self.assertIn("Travel tip added successfully!", self.driver.page_source)

        # Submit incomplete travel details
        self.driver.find_element(By.NAME, 'destination').clear()
        self.driver.find_element(By.NAME, 'tips').clear()
        self.driver.find_element(By.NAME, 'destination').send_keys("Paris")
        self.driver.find_element(By.XPATH, '//button[text()="Add Tip"]').click()
        time.sleep(1)

        # Check for error message
        self.assertIn("All fields are required.", self.driver.page_source)

    def test_view_recommendations(self):
        self.fail("Not implemented")

    def test_search_for_tips(self):
        self.fail("Not implemented")

    def test_save_favorite_travel_tips(self):
        self.fail("Not implemented")

    def test_user_logout(self):
        self.fail("Not implemented")

    def test_navigate_back_to_dashboard(self):
        self.fail("Not implemented")

    def test_view_saved_travel_tips(self):
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
