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
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:9042/')  # Navigate to the login page

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

        # Verify the Registration Page is displayed
        self.assertIn("Registration", self.driver.title)

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
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Registration", self.driver.title)

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:9042/')  # Navigate back to the login page
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)

    def test_manage_medical_information(self):
        # Log in successfully
        self.login("user1", "user123")

        # Verify the user can view their current medical information
        self.assertIn("Dashboard", self.driver.title)

        # Input new medical information and save
        self.driver.find_element(By.NAME, 'diagnoses').send_keys("Cold")
        self.driver.find_element(By.NAME, 'medications').send_keys("Paracetamol")
        self.driver.find_element(By.NAME, 'treatments').send_keys("Rest")
        self.driver.find_element(By.NAME, 'add_medical_info').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the new information is saved successfully
        self.assertIn("Dashboard", self.driver.title)

    def test_set_and_receive_appointment_reminders(self):
        # Log in successfully
        self.login("user1", "user123")

        # Verify the user can view existing appointment reminders
        self.assertIn("Dashboard", self.driver.title)

        # Set a new appointment reminder with a valid date and time
        self.driver.find_element(By.NAME, 'date').send_keys("2023-12-01")
        self.driver.find_element(By.NAME, 'time').send_keys("14:00")
        self.driver.find_element(By.NAME, 'set_appointment').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the reminder is saved successfully
        self.assertIn("Dashboard", self.driver.title)

    def test_user_logout(self):
        # Log in successfully
        self.login("user1", "user123")

        # Verify the Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Click the logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is logged out and redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:9042/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
