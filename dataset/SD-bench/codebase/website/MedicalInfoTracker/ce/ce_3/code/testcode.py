import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestMedicalInfoTracker(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8638/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and stop the application
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
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Username already exists", self.driver.page_source)

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8638/')  # Navigate back to the login page
        self.login("invalid_user", "wrong_password")

        # Verify an error message is displayed
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_manage_medical_information(self):
        # Log in successfully
        self.login("user1", "user123")

        # Verify the user can view their current medical information
        self.assertIn("Dashboard", self.driver.title)
        self.assertIn("Diabetes", self.driver.page_source)

        # Input new medical information and save
        self.driver.find_element(By.NAME, 'diagnosis').send_keys("Hypertension")
        self.driver.find_element(By.NAME, 'add_diagnosis').click()
        time.sleep(1)  # Wait for the page to refresh

        # Verify the new information is saved and displayed
        self.assertIn("Hypertension", self.driver.page_source)

    def test_set_and_receive_appointment_reminders(self):
        # Log in successfully
        self.login("user1", "user123")

        # Verify the user can view existing appointment reminders
        self.assertIn("Doctor's appointment on 2023-10-01", self.driver.page_source)

        # Set a new appointment reminder
        self.fail("Not implemented")  # Placeholder for functionality not implemented

    def test_view_and_edit_medical_history(self):
        # Log in successfully
        self.login("user1", "user123")

        # Verify the user can view their complete medical history
        self.assertIn("Diabetes", self.driver.page_source)

        # Attempt to delete a medical history entry
        self.fail("Not implemented")  # Placeholder for functionality not implemented

    def test_user_logout(self):
        # Log in successfully
        self.login("user1", "user123")

        # Click the logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8638/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
