import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestSportsEquipmentInventoryTracker(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8250/') 

    def tearDown(self):
        # Close the web driver session and terminate the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8250/register')
        
        # Verify Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8250/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("User already exists", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8250/')
        self.login("invalid_user", "invalid_password")

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_dashboard_equipment_management(self):
        # Functionality 3: Equipment Management on Dashboard Page
        self.login("admin", "admin123")

        # Verify that the equipment management interface is displayed
        self.assertIn("Equipment Dashboard", self.driver.title)

        # Add new equipment
        self.driver.find_element(By.NAME, 'add_equipment').click()  # Assuming there's a button to add equipment
        self.driver.find_element(By.NAME, 'name').send_keys("New Equipment")
        self.driver.find_element(By.NAME, 'type').send_keys("Tool")
        self.driver.find_element(By.NAME, 'quantity').send_keys("5")
        self.driver.find_element(By.NAME, 'condition').send_keys("Good")
        self.driver.find_element(By.NAME, 'location').send_keys("Warehouse A")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify that the new equipment is displayed in the list
        self.assertIn("New Equipment", self.driver.page_source)

        # Update existing equipment
        self.driver.find_element(By.NAME, 'update_equipment').click()  # Assuming there's a button to update equipment
        self.driver.find_element(By.NAME, 'name').send_keys("New Equipment")
        self.driver.find_element(By.NAME, 'quantity').clear()
        self.driver.find_element(By.NAME, 'quantity').send_keys("10")
        self.driver.find_element(By.XPATH, '//button[text()="Update"]').click()

        # Verify that the updated information is reflected
        self.assertIn("10", self.driver.page_source)

    def test_view_equipment_details(self):
        # Functionality 4: View Equipment Details
        self.login("admin", "admin123")

        # Click on a specific equipment item (assuming there's a way to do this)
        self.driver.find_element(By.LINK_TEXT, "New Equipment").click()  # Replace with actual link text

        # Verify detailed information about the selected equipment item
        self.assertIn("New Equipment", self.driver.page_source)

    def test_search_equipment(self):
        # Functionality 6: Search for Equipment
        self.login("admin", "admin123")

        # Search for equipment
        search_query = "New Equipment"
        self.driver.find_element(By.NAME, 'search').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that the equipment list is filtered
        self.assertIn("New Equipment", self.driver.page_source)

    def test_filter_equipment_list(self):
        # Functionality 7: Filter Equipment List
        self.login("admin", "admin123")

        # Apply a filter based on equipment condition
        self.driver.find_element(By.NAME, 'filter_condition').send_keys("Good")
        self.driver.find_element(By.XPATH, '//button[text()="Filter"]').click()

        # Verify that the equipment list updates
        self.assertIn("New Equipment", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_data_persistence(self):
        # Functionality 9: Data Persistence
        self.login("admin", "admin123")

        # Add a new equipment item
        self.driver.find_element(By.NAME, 'add_equipment').click()
        self.driver.find_element(By.NAME, 'name').send_keys("Persistent Equipment")
        self.driver.find_element(By.NAME, 'type').send_keys("Tool")
        self.driver.find_element(By.NAME, 'quantity').send_keys("5")
        self.driver.find_element(By.NAME, 'condition').send_keys("Good")
        self.driver.find_element(By.NAME, 'location').send_keys("Warehouse A")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Logout and close the application
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Reopen the application and log in again
        self.login("admin", "admin123")

        # Verify that the previously added equipment item is still present
        self.assertIn("Persistent Equipment", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
