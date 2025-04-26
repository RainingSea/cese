import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelTipperApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8262/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8262/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)  # Check if Registration Page is displayed

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8262/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Registration failed", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Travel Tips Input", self.driver.title)  # Check if redirected to the dashboard

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8262/')
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Login failed", self.driver.page_source)  # Check for error message

    def test_input_travel_details(self):
        # Functionality 3: Input Travel Details
        self.login("admin", "admin123")  # Log in first
        self.assertIn("Travel Tips Input", self.driver.title)  # Check if on the input page

        # Submit valid travel details
        self.driver.find_element(By.NAME, 'destination').send_keys("Paris")
        self.driver.find_element(By.NAME, 'tips').send_keys("Visit the Eiffel Tower")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tips"]').click()

        # Verify that the tips are displayed
        self.assertIn("Visit the Eiffel Tower", self.driver.page_source)

        # Attempt to submit incomplete details
        self.driver.find_element(By.NAME, 'destination').clear()
        self.driver.find_element(By.NAME, 'tips').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tips"]').click()

        # Verify error message for incomplete submission
        self.assertIn("All fields are required", self.driver.page_source)

    def test_view_recommendations(self):
        # Functionality 4: View Recommendations
        self.login("admin", "admin123")  # Log in first
        self.driver.find_element(By.NAME, 'destination').send_keys("New York")
        self.driver.find_element(By.NAME, 'tips').send_keys("Explore Central Park")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tips"]').click()

        # Verify that recommendations are displayed
        self.assertIn("Explore Central Park", self.driver.page_source)

    def test_search_for_tips(self):
        # Functionality 5: Search for Tips
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8262/travel_input')  # Navigate to travel input page

        # Search for tips
        self.driver.find_element(By.NAME, 'destination').send_keys("Paris")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that relevant tips are displayed
        self.assertIn("Visit the Eiffel Tower", self.driver.page_source)

        # Search for a non-existent destination
        self.driver.find_element(By.NAME, 'destination').clear()
        self.driver.find_element(By.NAME, 'destination').send_keys("NonExistentPlace")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify message for no tips found
        self.assertIn("No tips found", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Log in first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click logout
        self.assertIn("Login", self.driver.title)  # Verify redirection to login page

if __name__ == '__main__':
    unittest.main()
