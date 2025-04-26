import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelLogApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8268/')  # Use the port from main.py

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
        self.driver.get('http://localhost:8268/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "testuser"
        new_password = "testpass"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8268/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8268/')
        self.login("admin", "wrongpassword")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_create_journal_entry(self):
        # Functionality 3: Create and Save Travel Journal Entries
        self.login("admin", "admin123")  # Login first
        self.assertIn("Dashboard", self.driver.title)

        # Fill in the journal entry form
        self.driver.find_element(By.NAME, 'destination').send_keys("Paris")
        self.driver.find_element(By.NAME, 'dates').send_keys("2023-01-01 to 2023-01-07")
        self.driver.find_element(By.NAME, 'activities').send_keys("Sightseeing, Museums")
        self.driver.find_element(By.NAME, 'reflections').send_keys("Amazing experience!")
        self.driver.find_element(By.XPATH, '//button[text()="Add Entry"]').click()

        # Verify the entry is saved
        self.assertIn("Paris", self.driver.page_source)

        # Attempt to submit with missing required fields
        self.driver.find_element(By.NAME, 'destination').clear()  # Clear destination
        self.driver.find_element(By.XPATH, '//button[text()="Add Entry"]').click()
        self.assertIn("This field is required", self.driver.page_source)

    def test_view_entries(self):
        # Functionality 4: View and Organize Past Entries
        self.login("admin", "admin123")  # Login first
        self.assertIn("Dashboard", self.driver.title)

        # Verify that past entries are displayed
        entries = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(entries), 0, "No journal entries found.")

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")  # Login first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 9: Navigate Back to Dashboard
        self.login("admin", "admin123")  # Login first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.driver.get('http://localhost:8268/')  # Go back to login
        self.login("admin", "admin123")  # Login again
        self.assertIn("Dashboard", self.driver.title)

if __name__ == '__main__':
    unittest.main()
