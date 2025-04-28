import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMedicalInfoTrackerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8343/')  # Accessing the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        # Verify that the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter valid username and password
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8343/')  # Accessing the login page

        # Enter valid username and password
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8343/')  # Accessing the login page again
        self.login("admin", "wrongpassword")

        # Verify error message for incorrect credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_manage_medical_information(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows medical information
        self.assertIn("Your Medical Information", self.driver.page_source)

        # Input new medical information
        self.driver.find_element(By.NAME, 'diagnosis').send_keys("Cold")
        self.driver.find_element(By.XPATH, '//button[text()="Add Diagnosis"]').click()

        # Verify that the new information is displayed
        self.assertIn("Diagnosis: Cold", self.driver.page_source)

        # Attempt to edit existing medical information (not implemented)
        self.fail("Edit medical information functionality not implemented")

    def test_set_and_receive_appointment_reminders(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Set a new appointment reminder
        self.driver.find_element(By.NAME, 'reminder_date').send_keys("2023-12-01")
        self.driver.find_element(By.NAME, 'reminder_time').send_keys("10:00")
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()

        # Verify that the reminder is displayed
        self.assertIn("Reminder: 2023-12-01 at 10:00", self.driver.page_source)

        # Attempt to set an appointment reminder with an invalid date format (not implemented)
        self.fail("Invalid date format handling not implemented")

    def test_user_logout(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Click the logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8343/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
