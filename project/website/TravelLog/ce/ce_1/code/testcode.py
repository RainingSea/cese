import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelLogApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8267/')  # Use the port from main.py

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8267/register')
        
        # Check if the registration form is displayed
        self.assertIn("Register", self.driver.title)

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8267/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing user
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify error message for existing username
        self.assertIn("Registration failed", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8267/login')
        
        # Check if the login form is displayed
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Journal Entries", self.driver.page_source)  # Check for journal entry page content

        # Invalid login
        self.driver.get('http://localhost:8267/login')
        self.login("admin", "wrongpassword")
        self.assertIn("Login failed", self.driver.page_source)

    def test_create_journal_entry(self):
        # Functionality 3: Create and Save Travel Journal Entries
        self.login("admin", "admin123")
        
        # Check if the journal entry form is displayed
        self.assertIn("Journal Entries", self.driver.page_source)

        # Fill in the journal entry form
        self.driver.find_element(By.NAME, 'destination').send_keys("New York")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-09-01")
        self.driver.find_element(By.NAME, 'activities').send_keys("Visited Central Park")
        self.driver.find_element(By.NAME, 'reflections').send_keys("It was a lovely day!")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify that the entry is saved and displayed
        self.assertIn("New York", self.driver.page_source)

    def test_view_entries(self):
        # Functionality 4: View and Organize Past Entries
        self.login("admin", "admin123")
        
        # Check if past entries are displayed
        self.assertIn("Past Entries", self.driver.page_source)

    def test_edit_entry(self):
        # Functionality 5: Edit or Delete Travel Entries
        self.login("admin", "admin123")

        # Assuming there's a way to edit an entry (not implemented in the codebase)
        # This is a placeholder for the edit functionality
        self.fail("Edit functionality not implemented in the codebase.")

    def test_delete_entry(self):
        # Functionality 5: Edit or Delete Travel Entries
        self.login("admin", "admin123")

        # Assuming there's a way to delete an entry (not implemented in the codebase)
        # This is a placeholder for the delete functionality
        self.fail("Delete functionality not implemented in the codebase.")

    def test_search_entries(self):
        # Functionality 7: Search for Specific Entries or Destinations
        self.login("admin", "admin123")
        
        # Navigate to search page
        self.driver.get('http://localhost:8267/search')
        self.assertIn("Search Journal Entries", self.driver.page_source)

        # Perform a search
        self.driver.find_element(By.NAME, 'query').send_keys("Paris")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify search results
        self.assertIn("No entries found", self.driver.page_source)  # Assuming no entries match

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
