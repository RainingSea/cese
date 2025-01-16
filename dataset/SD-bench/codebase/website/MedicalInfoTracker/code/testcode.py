import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestMedicalInfoTracker(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8640/')

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
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that an error message is displayed
        self.assertIn("Username already exists!", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.page_source)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8640/')
        self.login("invalid_user", "invalid_pass")

        # Verify that an error message is displayed
        self.assertIn("Invalid username or password!", self.driver.page_source)

    def test_manage_medical_information(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify that the user can view their current medical information
        self.assertIn("Your Medical Information", self.driver.page_source)

        # Input new medical information and save
        self.driver.find_element(By.NAME, 'diagnoses').send_keys("cold")
        self.driver.find_element(By.NAME, 'medications').send_keys("aspirin")
        self.driver.find_element(By.NAME, 'treatments').send_keys("rest")
        self.driver.find_element(By.NAME, 'add_medical_info').click()
        time.sleep(1)  # Wait for the information to be saved

        # Verify that the new information is displayed
        self.assertIn("cold", self.driver.page_source)

    def test_set_and_receive_appointment_reminders(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify that the user can view existing appointment reminders
        self.assertIn("Your Appointments", self.driver.page_source)

        # Set a new appointment reminder with a valid date and time
        self.driver.find_element(By.NAME, 'date').send_keys("2023-12-01")
        self.driver.find_element(By.NAME, 'time').send_keys("15:00")
        self.driver.find_element(By.NAME, 'description').send_keys("Eye Checkup")
        self.driver.find_element(By.NAME, 'set_appointment').click()
        time.sleep(1)  # Wait for the appointment to be saved

        # Verify that the new appointment is displayed
        self.assertIn("Eye Checkup", self.driver.page_source)

        # Attempt to set an appointment reminder with an invalid date format
        self.driver.find_element(By.NAME, 'date').send_keys("invalid-date")
        self.driver.find_element(By.NAME, 'time').send_keys("15:00")
        self.driver.find_element(By.NAME, 'description').send_keys("Test Appointment")
        self.driver.find_element(By.NAME, 'set_appointment').click()
        time.sleep(1)  # Wait for the error message

        # Verify that an error message is displayed
        self.assertIn("Invalid date format", self.driver.page_source)

    def test_user_logout(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify that the Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.page_source)

        # Click the logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8640/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
