import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelLogApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the actual port from main.py

    def tearDown(self):
        # Close the web driver session and the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:5000/login')  # Navigate to login page
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:5000/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()

        # Verify registration success
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:5000/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Test invalid login
        self.driver.get('http://localhost:5000/login')
        self.driver.find_element(By.NAME, 'username').send_keys("invalid_user")
        self.driver.find_element(By.NAME, 'password').send_keys("wrong_password")
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_create_entry(self):
        # Functionality 3: Create and Save Travel Journal Entries
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/create_entry')  # Navigate to create entry page
        self.assertIn("Create Entry", self.driver.title)

        # Fill in the entry form
        self.driver.find_element(By.ID, 'destination').send_keys("Paris")
        self.driver.find_element(By.ID, 'dates').send_keys("2023-01-01 to 2023-01-10")
        self.driver.find_element(By.ID, 'activities').send_keys("Sightseeing")
        self.driver.find_element(By.ID, 'photos').send_keys("photo1.jpg")
        self.driver.find_element(By.ID, 'reflections').send_keys("Had a great time!")
        self.driver.find_element(By.XPATH, '//input[@value="Create Entry"]').click()

        # Verify entry creation success
        self.assertIn("Entry created successfully", self.driver.page_source)

        # Attempt to submit with missing required fields
        self.driver.get('http://localhost:5000/create_entry')
        self.driver.find_element(By.XPATH, '//input[@value="Create Entry"]').click()  # Submit empty form
        self.assertIn("This field is required", self.driver.page_source)

    def test_view_entries(self):
        # Functionality 4: View and Organize Past Entries
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/view_entries')  # Navigate to view entries page
        self.assertIn("Past Entries", self.driver.title)

        # Verify entries are displayed
        entries = self.driver.find_elements(By.CLASS_NAME, 'entry')
        self.assertGreater(len(entries), 0, "No journal entries found.")

    def test_edit_delete_entry(self):
        # Functionality 5: Edit or Delete Travel Entries
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/view_entries')  # Navigate to view entries page

        # Assuming the first entry is editable
        self.driver.find_element(By.XPATH, '//button[text()="Edit"]').click()  # Click edit on the first entry
        self.driver.find_element(By.ID, 'destination').clear()
        self.driver.find_element(By.ID, 'destination').send_keys("Updated Destination")
        self.driver.find_element(By.XPATH, '//input[@value="Save Entry"]').click()

        # Verify entry update success
        self.assertIn("Entry updated successfully", self.driver.page_source)

        # Delete the entry
        self.driver.get('http://localhost:5000/view_entries')
        self.driver.find_element(By.XPATH, '//button[text()="Delete"]').click()  # Click delete on the first entry
        self.assertIn("Entry deleted successfully", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_search_entries(self):
        # Functionality 7: Search for Specific Entries or Destinations
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/search')  # Navigate to search page
        self.assertIn("Search", self.driver.title)

        # Perform a search
        self.driver.find_element(By.NAME, 'query').send_keys("Paris")
        self.driver.find_element(By.XPATH, '//input[@value="Search"]').click()

        # Verify search results
        self.assertIn("Paris", self.driver.page_source)

        # Search for a non-existent entry
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys("NonExistent")
        self.driver.find_element(By.XPATH, '//input[@value="Search"]').click()
        self.assertIn("No entries found", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
