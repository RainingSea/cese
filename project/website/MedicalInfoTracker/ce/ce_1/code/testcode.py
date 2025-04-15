import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestMedicalInfoTracker(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8302/login')

    def tearDown(self):
        # Close the web driver session
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
        self.driver.get('http://localhost:8302/register')
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8302/register')
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that an error message is displayed
        error_message = self.driver.find_element(By.XPATH, '//p[@style="color:red;"]').text
        self.assertEqual(error_message, "Username already exists.")

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8302/login')
        self.login("invalid_user", "invalid_pass")

        # Verify that an error message is displayed
        self.assertIn("Login", self.driver.title)

    def test_manage_medical_information(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify that the user can view their current medical information
        self.assertIn("Dashboard", self.driver.title)

        # Input new medical information and save
        self.driver.find_element(By.NAME, 'diagnosis').send_keys('Test Diagnosis')
        self.driver.find_element(By.NAME, 'medication').send_keys('Test Medication')
        self.driver.find_element(By.NAME, 'treatment').send_keys('Test Treatment')
        self.driver.find_element(By.XPATH, '//button[text()="Add Medical Info"]').click()
        time.sleep(1)  # Wait for the page to reload

        # Verify that the new information is displayed
        self.assertIn("Test Diagnosis", self.driver.page_source)
        self.assertIn("Test Medication", self.driver.page_source)
        self.assertIn("Test Treatment", self.driver.page_source)

    def test_set_and_receive_appointment_reminders(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify that the user can view existing appointment reminders
        self.assertIn("Dashboard", self.driver.title)

        # Set a new appointment reminder with a valid date and time
        self.driver.find_element(By.NAME, 'date').send_keys('2023-11-01')
        self.driver.find_element(By.NAME, 'time').send_keys('10:00')
        self.driver.find_element(By.NAME, 'description').send_keys('Test Appointment')
        self.driver.find_element(By.XPATH, '//button[text()="Add Appointment"]').click()
        time.sleep(1)  # Wait for the page to reload

        # Verify that the reminder is displayed
        self.assertIn("2023-11-01 at 10:00: Test Appointment", self.driver.page_source)

    def test_user_logout(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Click the logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8302/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
