import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTravelLogApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8665/')

    def tearDown(self):
        # Close the web driver session and stop the Flask app
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
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register").click()
        time.sleep(1)

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.NAME, 'username').send_keys('newuser')
        self.driver.find_element(By.NAME, 'password').send_keys('newpassword')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register").click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Expectation: No change in page, indicating failure
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Enter a valid username and password
        self.login('admin', 'admin123')

        # Verify redirection to the Journal Page
        self.assertIn("Travel Journal", self.driver.page_source)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8665/')
        self.login('invaliduser', 'invalidpass')

        # Expectation: Redirected back to login page
        self.assertIn("Login", self.driver.title)

    def test_create_and_save_journal_entries(self):
        self.login('admin', 'admin123')

        # Fill in the form with valid details and submit
        self.driver.find_element(By.NAME, 'destination').send_keys('New York')
        self.driver.find_element(By.NAME, 'date').send_keys('2023-10-10')
        self.driver.find_element(By.NAME, 'activities').send_keys('Visited Central Park')
        self.driver.find_element(By.NAME, 'photos').send_keys('central_park.jpg')
        self.driver.find_element(By.NAME, 'reflections').send_keys('It was amazing!')
        self.driver.find_element(By.XPATH, '//button[text()="Save Entry"]').click()
        time.sleep(1)

        # Verify the entry is saved successfully
        self.assertIn('New York', self.driver.page_source)

        # Attempt to submit the form with missing required fields
        self.driver.find_element(By.NAME, 'destination').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Save Entry"]').click()
        time.sleep(1)

        # Expectation: Still on the same page due to validation failure
        self.assertIn("Travel Journal", self.driver.page_source)

    def test_user_logout(self):
        self.login('admin', 'admin123')

        # Click the "Logout" button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Journal Page after logging out
        self.driver.get('http://localhost:8665/journal')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
