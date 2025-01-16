import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTravelLogApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8666/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and stop the Flask application
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

        # Verify the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Create Account"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Create Account"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Verify the Login form is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8666/')  # Navigate back to the login page
        self.login("invalid_user", "wrong_password")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)

    def test_create_and_save_travel_journal_entries(self):
        # Log in to the user account
        self.login("admin", "admin123")

        # Verify the Journal Entry form is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Fill in the form with valid details and submit
        self.driver.find_element(By.NAME, 'destination').send_keys("London")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-10")
        self.driver.find_element(By.NAME, 'activities').send_keys("Visited the Tower of London")
        self.driver.find_element(By.NAME, 'photos').send_keys("photo3.jpg")
        self.driver.find_element(By.NAME, 'reflections').send_keys("It was amazing!")
        self.driver.find_element(By.XPATH, '//button[text()="Add Entry"]').click()
        time.sleep(1)  # Wait for the entry to be saved

        # Verify the entry is saved successfully
        self.assertIn("London", self.driver.page_source)

        # Attempt to submit the form with missing required fields
        self.driver.find_element(By.NAME, 'destination').clear()
        self.driver.find_element(By.NAME, 'date').clear()
        self.driver.find_element(By.NAME, 'activities').clear()
        self.driver.find_element(By.NAME, 'reflections').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Add Entry"]').click()
        time.sleep(1)  # Wait for the error message

        # Verify an error message is displayed
        self.assertIn("Dashboard", self.driver.title)

    def test_user_logout(self):
        # Log in to the user account
        self.login("admin", "admin123")

        # Click the "Logout" button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is logged out and redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8666/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
