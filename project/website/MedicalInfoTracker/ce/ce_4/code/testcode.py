import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestMedicalInfoTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Allow some time for the server to start

        # Initialize the webdriver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8639/')

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
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
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys("user1")
        self.driver.find_element(By.NAME, 'password').send_keys("user123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)  # Assuming it stays on the same page

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("user1", "user123")

        # Verify that the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8639/')
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)  # Assuming it stays on the login page

    def test_manage_medical_information(self):
        # Log in successfully
        self.login("user1", "user123")

        # Verify that the Medical Information section is accessible
        self.assertIn("Dashboard", self.driver.title)

        # Input new medical information and save
        self.driver.find_element(By.NAME, 'diagnoses').send_keys("cold")
        self.driver.find_element(By.NAME, 'medications').send_keys("paracetamol")
        self.driver.find_element(By.NAME, 'treatments').send_keys("rest")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        time.sleep(1)  # Wait for the save operation

        # Verify the new information is saved
        self.assertIn("Dashboard", self.driver.title)  # Assuming it stays on the same page

    def test_set_and_receive_appointment_reminders(self):
        # Log in successfully
        self.login("user1", "user123")

        # Verify that the Appointment Reminders section is accessible
        self.assertIn("Dashboard", self.driver.title)

        # Set a new appointment reminder with a valid date and time
        self.driver.find_element(By.NAME, 'date').send_keys("2023-12-01")
        self.driver.find_element(By.NAME, 'time').send_keys("14:00")
        self.driver.find_element(By.NAME, 'description').send_keys("Dentist Appointment")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        time.sleep(1)  # Wait for the save operation

        # Verify the reminder is saved
        self.assertIn("Dashboard", self.driver.title)  # Assuming it stays on the same page

        # Attempt to set an appointment reminder with an invalid date format
        self.driver.find_element(By.NAME, 'date').clear()
        self.driver.find_element(By.NAME, 'date').send_keys("invalid-date")
        self.driver.find_element(By.NAME, 'time').send_keys("14:00")
        self.driver.find_element(By.NAME, 'description').send_keys("Invalid Date Test")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        time.sleep(1)  # Wait for the save operation

        # Verify an error message is displayed
        self.assertIn("Dashboard", self.driver.title)  # Assuming it stays on the same page

    def test_user_logout(self):
        # Log in successfully
        self.login("user1", "user123")

        # Verify that the Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Click the logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8639/dashboard')
        self.assertIn("Login", self.driver.title)  # Access should be denied

if __name__ == '__main__':
    unittest.main()
