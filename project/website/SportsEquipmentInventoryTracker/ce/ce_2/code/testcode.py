import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestSportsEquipmentInventoryTracker(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8424/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8424/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)  # Check if Registration form is displayed

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8424/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)  # Check if redirected to Dashboard

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8424/')
        self.login("invalid_user", "wrong_password")
        self.assertIn("Invalid credentials", self.driver.page_source)  # Check for error message

    def test_equipment_management(self):
        # Functionality 3: Equipment Management on Dashboard Page
        self.login("admin", "admin123")  # Login successfully
        self.assertIn("Dashboard", self.driver.title)  # Check if Dashboard is displayed

        # Add new equipment
        self.driver.find_element(By.NAME, 'name').send_keys("New Equipment")
        self.driver.find_element(By.NAME, 'quantity').send_keys("10")
        self.driver.find_element(By.NAME, 'condition').send_keys("Good")
        self.driver.find_element(By.NAME, 'location').send_keys("Warehouse A")
        self.driver.find_element(By.XPATH, '//button[text()="Add Equipment"]').click()

        # Verify that the new equipment is displayed in the list
        self.assertIn("New Equipment", self.driver.page_source)

    def test_view_equipment_details(self):
        # Functionality 4: View Equipment Details
        self.login("admin", "admin123")  # Login successfully
        self.assertIn("Dashboard", self.driver.title)  # Check if Dashboard is displayed

        # Check if equipment list is displayed
        equipment_list = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(equipment_list), 0, "No equipment found.")

    def test_search_equipment(self):
        # Functionality 6: Search for Equipment
        self.login("admin", "admin123")  # Login successfully
        self.assertIn("Dashboard", self.driver.title)  # Check if Dashboard is displayed

        # Search for equipment
        search_query = "Drill"
        self.driver.find_element(By.NAME, 'search').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that the search results are displayed
        self.assertIn(search_query, self.driver.page_source)

    def test_filter_equipment(self):
        # Functionality 7: Filter Equipment List
        self.login("admin", "admin123")  # Login successfully
        self.assertIn("Dashboard", self.driver.title)  # Check if Dashboard is displayed

        # Apply filter
        self.driver.find_element(By.NAME, 'filter_condition').send_keys("Good")
        self.driver.find_element(By.XPATH, '//button[text()="Filter"]').click()

        # Verify that the filtered results are displayed
        self.assertIn("Good", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")  # Login successfully
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click Logout
        self.assertIn("Login", self.driver.title)  # Verify redirection to Login Page

    def test_data_persistence(self):
        # Functionality 9: Data Persistence
        self.login("admin", "admin123")  # Login successfully
        self.driver.find_element(By.NAME, 'name').send_keys("Persistent Equipment")
        self.driver.find_element(By.NAME, 'quantity').send_keys("5")
        self.driver.find_element(By.NAME, 'condition').send_keys("Excellent")
        self.driver.find_element(By.NAME, 'location').send_keys("Warehouse B")
        self.driver.find_element(By.XPATH, '//button[text()="Add Equipment"]').click()

        # Logout and log back in
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.login("admin", "admin123")

        # Verify that the previously added equipment is still present
        self.assertIn("Persistent Equipment", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
