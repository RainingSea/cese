import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestVehicleMaintenanceTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8452/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8452/register')  # Navigate to registration page

        # Check if registration page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter valid username and password
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8452/register')  # Navigate to registration page
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials

        # Verify redirection to the dashboard (vehicle_info page)
        self.assertIn("Vehicle Information", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8452/')  # Navigate to login page
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("wrong_password")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_input_vehicle_information(self):
        # Functionality 3: Input Vehicle Information
        self.login("admin", "admin123")  # Log in successfully
        self.driver.get('http://localhost:8452/vehicle_info')  # Navigate to vehicle info page

        # Check if vehicle info page is displayed
        self.assertIn("Vehicle Information", self.driver.title)

        # Enter valid vehicle information
        self.driver.find_element(By.NAME, 'make').send_keys("Ford")
        self.driver.find_element(By.NAME, 'model').send_keys("Focus")
        self.driver.find_element(By.NAME, 'year').send_keys("2021")
        self.driver.find_element(By.NAME, 'mileage').send_keys("10000")
        self.driver.find_element(By.XPATH, '//button[text()="Add Vehicle"]').click()

        # Verify vehicle information is saved
        self.assertIn("Ford Focus", self.driver.page_source)

        # Attempt to enter invalid vehicle information (negative mileage)
        self.driver.find_element(By.NAME, 'make').send_keys("Toyota")
        self.driver.find_element(By.NAME, 'model').send_keys("Corolla")
        self.driver.find_element(By.NAME, 'year').send_keys("2022")
        self.driver.find_element(By.NAME, 'mileage').send_keys("-5000")  # Invalid mileage
        self.driver.find_element(By.XPATH, '//button[text()="Add Vehicle"]').click()

        # Verify error message for invalid input
        self.assertIn("Invalid input", self.driver.page_source)

    def test_track_regular_maintenance_tasks(self):
        # Functionality 4: Track Regular Maintenance Tasks
        self.login("admin", "admin123")  # Log in successfully
        self.driver.get('http://localhost:8452/maintenance')  # Navigate to maintenance page

        # Check if maintenance page is displayed
        self.assertIn("Maintenance Tracking", self.driver.title)

        # Enter valid maintenance task
        self.driver.find_element(By.NAME, 'vehicle_id').send_keys("1")
        self.driver.find_element(By.NAME, 'task').send_keys("Oil Change")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-01-15")
        self.driver.find_element(By.XPATH, '//button[text()="Add Record"]').click()

        # Verify maintenance task is saved
        self.assertIn("Oil Change", self.driver.page_source)

        # Attempt to add a maintenance task without specifying a task type
        self.driver.find_element(By.NAME, 'vehicle_id').send_keys("1")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-01-20")  # No task specified
        self.driver.find_element(By.XPATH, '//button[text()="Add Record"]').click()

        # Verify error message for missing task type
        self.assertIn("Task type is required", self.driver.page_source)

    def test_view_maintenance_history(self):
        # Functionality 6: View Maintenance History
        self.login("admin", "admin123")  # Log in successfully
        self.driver.get('http://localhost:8452/maintenance')  # Navigate to maintenance page

        # Check if maintenance history is displayed
        self.assertIn("Maintenance Tracking", self.driver.title)

        # Verify existing maintenance records are displayed
        self.assertIn("Oil Change", self.driver.page_source)
        self.assertIn("Tire Rotation", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")  # Log in successfully
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click logout button

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
