import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestSportsEquipmentInventoryTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8251/')  # Access the login page

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
        self.driver.get('http://localhost:8251/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8251/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8251/')
        self.login("admin", "wrong_password")  # Invalid password
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_dashboard_equipment_management(self):
        # Functionality 3: Equipment Management on Dashboard Page
        self.login("admin", "admin123")  # Log in successfully
        self.assertIn("Dashboard", self.driver.title)

        # Add new equipment
        self.driver.find_element(By.LINK_TEXT, 'Add Equipment').click()  # Assuming there's a link to add equipment
        self.driver.find_element(By.NAME, 'name').send_keys("New Hammer")
        self.driver.find_element(By.NAME, 'type').send_keys("Tool")
        self.driver.find_element(By.NAME, 'quantity').send_keys("10")
        self.driver.find_element(By.NAME, 'condition').send_keys("New")
        self.driver.find_element(By.NAME, 'availability').send_keys("true")
        self.driver.find_element(By.NAME, 'location').send_keys("Workshop")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify that the new equipment is displayed
        self.assertIn("New Hammer", self.driver.page_source)

        # Update existing equipment
        self.driver.find_element(By.LINK_TEXT, 'Edit Hammer').click()  # Assuming there's a link to edit equipment
        self.driver.find_element(By.NAME, 'quantity').clear()
        self.driver.find_element(By.NAME, 'quantity').send_keys("15")
        self.driver.find_element(By.XPATH, '//button[text()="Update"]').click()

        # Verify that the updated information is reflected
        self.assertIn("15", self.driver.page_source)

    def test_view_equipment_details(self):
        # Functionality 4: View Equipment Details
        self.login("admin", "admin123")  # Log in successfully
        self.driver.get('http://localhost:8251/dashboard')  # Navigate to Dashboard Page

        # Click on a specific equipment item
        self.driver.find_element(By.LINK_TEXT, 'Hammer').click()  # Assuming there's a link to view Hammer details
        self.assertIn("Hammer", self.driver.page_source)

    def test_set_alerts(self):
        # Functionality 5: Set Alerts for Equipment Maintenance
        self.login("admin", "admin123")  # Log in successfully
        self.driver.get('http://localhost:8251/dashboard')  # Navigate to Dashboard Page

        # Set a maintenance alert for an equipment item
        self.driver.find_element(By.LINK_TEXT, 'Hammer').click()  # Click on Hammer
        self.driver.find_element(By.XPATH, '//button[text()="Set Alert"]').click()  # Assuming there's a button to set alert
        self.assertIn("Alert set for Hammer", self.driver.page_source)

    def test_search_equipment(self):
        # Functionality 6: Search for Equipment
        self.login("admin", "admin123")  # Log in successfully
        self.driver.get('http://localhost:8251/dashboard')  # Navigate to Dashboard Page

        # Search for equipment
        self.driver.find_element(By.NAME, 'search').send_keys("Hammer")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.assertIn("Hammer", self.driver.page_source)

    def test_filter_equipment(self):
        # Functionality 7: Filter Equipment List
        self.login("admin", "admin123")  # Log in successfully
        self.driver.get('http://localhost:8251/dashboard')  # Navigate to Dashboard Page

        # Apply a filter based on equipment condition
        self.driver.find_element(By.NAME, 'filter').send_keys("New")
        self.driver.find_element(By.XPATH, '//button[text()="Filter"]').click()
        self.assertIn("New Hammer", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")  # Log in successfully
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Assuming there's a Logout link
        self.assertIn("Login", self.driver.title)

    def test_data_persistence(self):
        # Functionality 9: Data Persistence
        self.login("admin", "admin123")  # Log in successfully
        self.driver.get('http://localhost:8251/dashboard')  # Navigate to Dashboard Page

        # Add a new equipment item
        self.driver.find_element(By.LINK_TEXT, 'Add Equipment').click()
        self.driver.find_element(By.NAME, 'name').send_keys("Persistent Equipment")
        self.driver.find_element(By.NAME, 'type').send_keys("Tool")
        self.driver.find_element(By.NAME, 'quantity').send_keys("5")
        self.driver.find_element(By.NAME, 'condition').send_keys("New")
        self.driver.find_element(By.NAME, 'availability').send_keys("true")
        self.driver.find_element(By.NAME, 'location').send_keys("Workshop")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Logout and log back in
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.login("admin", "admin123")  # Log in again
        self.driver.get('http://localhost:8251/dashboard')  # Navigate to Dashboard Page

        # Verify that the previously added equipment is still present
        self.assertIn("Persistent Equipment", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
