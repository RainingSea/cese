import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestMedicalInfoTrackerApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8344/') 

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

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8344/register')
        self.assertIn("Register", self.driver.title)

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8344/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for existing username
        self.assertIn("Username already exists", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Medical Information page
        self.assertIn("Medical Information", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8344/')
        self.login("admin", "wrongpassword")
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_manage_medical_info(self):
        # Functionality 3: Manage Medical Information
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8344/medical_info')

        # Verify that the current medical information is displayed
        self.assertIn("Your Medical Information", self.driver.page_source)

        # Input new medical information
        self.driver.find_element(By.NAME, 'diagnosis').send_keys("Cold")
        self.driver.find_element(By.NAME, 'medication').send_keys("Cough Syrup")
        self.driver.find_element(By.NAME, 'treatment').send_keys("Rest and hydration")
        self.driver.find_element(By.XPATH, '//button[text()="Add Info"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the new information is displayed
        self.assertIn("Cold", self.driver.page_source)

    def test_set_reminders(self):
        # Functionality 4: Set and Receive Appointment Reminders
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8344/reminders')

        # Verify that existing reminders are displayed
        self.assertIn("Appointment Reminders", self.driver.page_source)

        # Set a new reminder
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-20")
        self.driver.find_element(By.NAME, 'time').send_keys("10:00")
        self.driver.find_element(By.NAME, 'description').send_keys("Check-up")
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the new reminder is displayed
        self.assertIn("Check-up", self.driver.page_source)

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8344/medical_info')

        # Simulate logout (assuming there's a logout button)
        self.driver.find_element(By.LINK_TEXT, 'View Reminders').click()  # Navigate to reminders
        self.driver.find_element(By.LINK_TEXT, 'Manage Medical Info').click()  # Navigate back to medical info
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Simulate logout
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
