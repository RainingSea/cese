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
        self.driver.get('http://localhost:9044/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.ID, 'username').send_keys(new_username)
        self.driver.find_element(By.ID, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.ID, 'username').send_keys(new_username)
        self.driver.find_element(By.ID, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Expectation: An error message is displayed indicating that the username is already taken
        # Note: The current implementation does not handle this case, so this will fail
        self.fail("Username already taken error handling not implemented")

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:9044/')  # Navigate back to the login page
        self.login("invalid_user", "invalid_pass")

        # Expectation: An error message is displayed indicating that the credentials are incorrect
        # Note: The current implementation does not handle this case, so this will fail
        self.fail("Invalid credentials error handling not implemented")

    def test_manage_medical_information(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify that the user can view their current medical information
        self.assertIn("Dashboard", self.driver.title)
        history_items = self.driver.find_elements(By.XPATH, '//ul[1]/li')
        self.assertGreater(len(history_items), 0, "No medical history found.")

        # Input new medical information and save
        # Note: The current implementation does not support adding new medical information, so this will fail
        self.fail("Adding new medical information not implemented")

    def test_set_and_receive_appointment_reminders(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify that the user can view existing appointment reminders
        self.assertIn("Dashboard", self.driver.title)
        reminder_items = self.driver.find_elements(By.XPATH, '//ul[2]/li')
        self.assertGreater(len(reminder_items), 0, "No appointment reminders found.")

        # Set a new appointment reminder
        # Note: The current implementation does not support setting new appointment reminders, so this will fail
        self.fail("Setting new appointment reminders not implemented")

    def test_view_and_edit_medical_history(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify that the user can view their complete medical history
        self.assertIn("Dashboard", self.driver.title)
        history_items = self.driver.find_elements(By.XPATH, '//ul[1]/li')
        self.assertGreater(len(history_items), 0, "No medical history found.")

        # Attempt to delete a medical history entry
        # Note: The current implementation does not support deleting medical history entries, so this will fail
        self.fail("Deleting medical history entries not implemented")

    def test_user_logout(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify that the Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Click the logout button
        # Note: The current implementation does not have a logout button, so this will fail
        self.fail("Logout functionality not implemented")

if __name__ == '__main__':
    unittest.main()
