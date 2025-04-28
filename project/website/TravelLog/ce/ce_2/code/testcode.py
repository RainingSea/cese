import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTravelLogApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8440/')  # Accessing the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
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
        self.driver.get('http://localhost:8440/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)  # Check if the Registration form is displayed

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.get('http://localhost:8440/register')  # Navigate to Registration Page
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that an error message is displayed
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials

        # Verify that the user is redirected to the Journal Entry Page
        self.assertIn("Journal Entry", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8440/')  # Navigate to Login Page
        self.driver.find_element(By.NAME, 'username').send_keys("invalid_user")
        self.driver.find_element(By.NAME, 'password').send_keys("invalid_password")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that an error message is displayed
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_create_journal_entry(self):
        # Functionality 3: Create and Save Travel Journal Entries
        self.login("admin", "admin123")  # Log in first

        # Verify that the Journal Entry form is displayed
        self.assertIn("Journal Entry", self.driver.title)

        # Fill in the form with valid details
        self.driver.find_element(By.NAME, 'destination').send_keys("Paris")
        self.driver.find_element(By.NAME, 'dates').send_keys("2023-06-01 to 2023-06-10")
        self.driver.find_element(By.NAME, 'activities').send_keys("Sightseeing, Dining")
        self.driver.find_element(By.NAME, 'reflections').send_keys("Amazing experience!")
        # Simulate file upload (assuming a valid file path)
        self.driver.find_element(By.NAME, 'photos').send_keys(r"D:\Project\ATEdev\ATEDev_main\project\website\TravelLog\ce\ce_2\code\static\uploads\paris_trip.jpg")
        self.driver.find_element(By.XPATH, '//button[text()="Add Entry"]').click()
        time.sleep(1)  # Wait for the entry to be saved

        # Verify that the entry is saved successfully
        self.assertIn("Paris", self.driver.page_source)

        # Attempt to submit the form with missing required fields
        self.driver.find_element(By.NAME, 'destination').clear()  # Clear destination field
        self.driver.find_element(By.XPATH, '//button[text()="Add Entry"]').click()
        time.sleep(1)  # Wait for the error message

        # Verify that an error message is displayed
        self.assertIn("This field is required", self.driver.page_source)

    def test_view_journal_entries(self):
        # Functionality 4: View and Organize Past Entries
        self.login("admin", "admin123")  # Log in first

        # Verify that the past entries are displayed
        entries = self.driver.find_elements(By.TAG_NAME, 'li')  # Assuming entries are in <li> tags
        self.assertGreater(len(entries), 0, "No journal entries found.")

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")  # Log in first

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
