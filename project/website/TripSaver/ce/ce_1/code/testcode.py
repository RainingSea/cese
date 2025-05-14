import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestTripSaverApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the Flask application
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        # Stop the Flask application
        cls.process.terminate()

    def setUp(self):
        # Initialize the webdriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8076/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        # Wait for redirect to trip_input page
        self.wait.until(EC.title_contains("Plan Your Trip"))

    def test_functionality_1_user_registration(self):
        """Test User Registration functionality"""
        # Navigate to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.wait.until(EC.title_contains("Registration"))
        
        # Test registration with new user
        username = "testuser_" + str(int(time.time()))
        password = "testpass123"
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.ID, 'confirm_password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        # Should redirect to login page
        self.wait.until(EC.title_contains("Login"))
        
        # Test registration with existing user
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.wait.until(EC.title_contains("Registration"))
        self.driver.find_element(By.ID, 'username').send_keys("user1")
        self.driver.find_element(By.ID, 'password').send_keys("password1")
        self.driver.find_element(By.ID, 'confirm_password').send_keys("password1")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        # Should stay on registration page (no redirect)
        self.assertTrue("Registration" in self.driver.title)

    def test_functionality_2_user_login(self):
        """Test User Login functionality"""
        # Test successful login
        self.login("user1", "password1")
        self.assertTrue("Plan Your Trip" in self.driver.title)
        
        # Logout by going back to login page
        self.driver.get('http://localhost:8076/login')
        
        # Test failed login
        self.driver.find_element(By.ID, 'username').send_keys("wronguser")
        self.driver.find_element(By.ID, 'password').send_keys("wrongpass")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        
        # Should stay on login page
        self.assertTrue("Login" in self.driver.title)

    def test_functionality_3_input_trip_details(self):
        """Test Input Trip Details functionality"""
        self.login("user1", "password1")
        
        # Test valid trip submission
        self.driver.find_element(By.ID, 'start').send_keys("New York")
        self.driver.find_element(By.ID, 'destination').send_keys("Boston")
        self.driver.find_element(By.ID, 'date').send_keys("2023-12-25")
        self.driver.find_element(By.XPATH, '//button[text()="Find Options"]').click()
        
        # Should redirect to results page
        self.wait.until(EC.title_contains("Transportation Options"))
        
        # Test invalid submission (empty fields)
        self.driver.get('http://localhost:8076/trip_input')
        self.driver.find_element(By.XPATH, '//button[text()="Find Options"]').click()
        
        # Should stay on trip input page
        self.assertTrue("Plan Your Trip" in self.driver.title)

    def test_functionality_4_view_transportation_suggestions(self):
        """Test View Transportation Suggestions functionality"""
        self.login("user1", "password1")
        
        # Submit trip details
        self.driver.find_element(By.ID, 'start').send_keys("Chicago")
        self.driver.find_element(By.ID, 'destination').send_keys("Miami")
        self.driver.find_element(By.ID, 'date').send_keys("2023-12-25")
        self.driver.find_element(By.XPATH, '//button[text()="Find Options"]').click()
        
        # Wait for results page
        self.wait.until(EC.title_contains("Transportation Options"))
        
        # Verify options are displayed
        options = self.driver.find_elements(By.XPATH, '//table/tbody/tr')
        self.assertGreater(len(options), 0, "No transportation options displayed")

    def test_functionality_5_save_preferred_transportation_options(self):
        """Test Save Preferred Transportation Options functionality"""
        self.login("user1", "password1")
        
        # Submit trip details
        self.driver.find_element(By.ID, 'start').send_keys("Los Angeles")
        self.driver.find_element(By.ID, 'destination').send_keys("San Francisco")
        self.driver.find_element(By.ID, 'date').send_keys("2023-12-25")
        self.driver.find_element(By.XPATH, '//button[text()="Find Options"]').click()
        
        # Wait for results page
        self.wait.until(EC.title_contains("Transportation Options"))
        
        # Save first option
        save_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Save"]')
        save_buttons[0].click()
        
        # Go to preferences page
        self.driver.get('http://localhost:8076/preferences')
        self.wait.until(EC.title_contains("Saved Preferences"))
        
        # Verify preference is saved
        preferences = self.driver.find_elements(By.XPATH, '//table/tbody/tr')
        self.assertGreater(len(preferences), 0, "No preferences saved")

    def test_functionality_6_user_logout(self):
        """Test User Logout functionality"""
        self.login("user1", "password1")
        
        # Logout by going to login page
        self.driver.get('http://localhost:8076/login')
        
        # Try to access trip input page directly
        self.driver.get('http://localhost:8076/trip_input')
        
        # Should be redirected back to login page
        self.assertTrue("Login" in self.driver.title)

    def test_functionality_7_view_estimated_costs_and_travel_times(self):
        """Test View Estimated Costs and Travel Times functionality"""
        self.login("user1", "password1")
        
        # Submit trip details
        self.driver.find_element(By.ID, 'start').send_keys("Seattle")
        self.driver.find_element(By.ID, 'destination').send_keys("Portland")
        self.driver.find_element(By.ID, 'date').send_keys("2023-12-25")
        self.driver.find_element(By.XPATH, '//button[text()="Find Options"]').click()
        
        # Wait for results page
        self.wait.until(EC.title_contains("Transportation Options"))
        
        # Verify cost and time are displayed for each option
        costs = self.driver.find_elements(By.XPATH, '//td[contains(text(), "$")]')
        times = self.driver.find_elements(By.XPATH, '//td[contains(text(), "hour")]')
        self.assertGreater(len(costs), 0, "No costs displayed")
        self.assertGreater(len(times), 0, "No travel times displayed")

    def test_functionality_8_compare_transportation_options(self):
        """Test Compare Transportation Options functionality"""
        self.login("user1", "password1")
        
        # Submit trip details
        self.driver.find_element(By.ID, 'start').send_keys("Dallas")
        self.driver.find_element(By.ID, 'destination').send_keys("Houston")
        self.driver.find_element(By.ID, 'date').send_keys("2023-12-25")
        self.driver.find_element(By.XPATH, '//button[text()="Find Options"]').click()
        
        # Wait for results page
        self.wait.until(EC.title_contains("Transportation Options"))
        
        # Select two options to compare
        selects = self.driver.find_elements(By.TAG_NAME, 'select')
        selects[0].find_elements(By.TAG_NAME, 'option')[0].click()
        selects[1].find_elements(By.TAG_NAME, 'option')[1].click()
        self.driver.find_element(By.XPATH, '//button[text()="Compare"]').click()
        
        # Verify comparison page
        self.wait.until(EC.title_contains("Comparison"))
        comparison = self.driver.find_elements(By.XPATH, '//div[@class="card"]')
        self.assertEqual(len(comparison), 2, "Comparison not displayed correctly")

if __name__ == '__main__':
    unittest.main()
