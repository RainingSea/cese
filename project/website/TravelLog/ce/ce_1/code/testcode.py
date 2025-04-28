import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelLogApp(unittest.TestCase):

    def setUp(self):
        # Start the main application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the correct port

    def tearDown(self):
        # Close the web driver session and the application process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:5000/login')  # Navigate to login page
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:5000/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:5000/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:5000/login')
        self.driver.find_element(By.NAME, 'username').send_keys("invalid_user")
        self.driver.find_element(By.NAME, 'password').send_keys("wrong_password")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

        # Verify error message for incorrect credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_create_entry(self):
        # Functionality 3: Create and Save Travel Journal Entries
        self.login("admin", "admin123")

        # Navigate to the Journal Entry Page
        self.driver.get('http://localhost:5000/create_entry')  # Assuming this is the correct URL

        # Fill in the form with valid details
        self.driver.find_element(By.NAME, 'destination').send_keys("Paris")
        self.driver.find_element(By.NAME, 'dates').send_keys("2023-06-01 to 2023-06-10")
        self.driver.find_element(By.NAME, 'activities').send_keys("Sightseeing, Dining")
        self.driver.find_element(By.NAME, 'photos').send_keys("photo1.jpg")
        self.driver.find_element(By.NAME, 'reflections').send_keys("Had an amazing time!")
        self.driver.find_element(By.XPATH, '//button[text()="Create Entry"]').click()

        # Verify that the entry is saved successfully
        self.assertIn("Entry created successfully", self.driver.page_source)

        # Attempt to submit the form with missing required fields
        self.driver.get('http://localhost:5000/create_entry')
        self.driver.find_element(By.XPATH, '//button[text()="Create Entry"]').click()  # Submit empty form

        # Verify error message for required fields
        self.assertIn("This field is required", self.driver.page_source)

    def test_view_entries(self):
        # Functionality 4: View and Organize Past Entries
        self.login("admin", "admin123")

        # Navigate to Past Entries Page
        self.driver.get('http://localhost:5000/past_entries')  # Assuming this is the correct URL

        # Verify that a list of past entries is displayed
        entries = self.driver.find_elements(By.TAG_NAME, 'li')  # Assuming entries are in <li> tags
        self.assertGreater(len(entries), 0, "No journal entries found.")

    def test_edit_delete_entry(self):
        # Functionality 5: Edit or Delete Travel Entries
        self.login("admin", "admin123")

        # Navigate to Past Entries Page
        self.driver.get('http://localhost:5000/past_entries')

        # Edit an entry (assuming the first entry is editable)
        self.driver.find_element(By.XPATH, '//button[text()="Edit"]').click()  # Click edit on the first entry
        self.driver.find_element(By.NAME, 'destination').clear()
        self.driver.find_element(By.NAME, 'destination').send_keys("Updated Destination")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()

        # Verify that the entry is updated successfully
        self.assertIn("Entry updated successfully", self.driver.page_source)

        # Delete an entry (assuming the first entry is deletable)
        self.driver.get('http://localhost:5000/past_entries')
        self.driver.find_element(By.XPATH, '//button[text()="Delete"]').click()  # Click delete on the first entry

        # Verify that the entry is deleted successfully
        self.assertIn("Entry deleted successfully", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 9: Navigate Back to Dashboard
        self.login("admin", "admin123")

        # Navigate to a specific travel entry
        self.driver.get('http://localhost:5000/past_entries')
        self.driver.find_element(By.XPATH, '//button[text()="View"]').click()  # Click view on the first entry

        # Click the "Back to Dashboard" button
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()

        # Verify that the user is back on the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

if __name__ == '__main__':
    unittest.main()
