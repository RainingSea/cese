import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestTripSaverApp(unittest.TestCase):
    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8077/')
        time.sleep(2)  # Wait for the server to start

    def tearDown(self):
        # Close the web driver session and stop the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        """Functionality 1: User Registration"""
        # Navigate to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        
        # Verify registration page is displayed
        self.assertIn("Register", self.driver.title)
        self.assertTrue(self.driver.find_element(By.NAME, 'username').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'password').is_displayed())
        
        # Test successful registration
        self.driver.find_element(By.NAME, 'username').send_keys('newuser')
        self.driver.find_element(By.NAME, 'password').send_keys('newpass123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)  # Should redirect to login
        
        # Test registration with existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        self.assertIn("Username already exists", self.driver.page_source)

    def test_user_login(self):
        """Functionality 2: User Login"""
        # Verify login page is displayed
        self.assertIn("Login", self.driver.title)
        self.assertTrue(self.driver.find_element(By.NAME, 'username').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'password').is_displayed())
        
        # Test successful login
        self.login("admin", "admin123")
        self.assertIn("Trip Planner", self.driver.title)  # Should redirect to trip planner
        
        # Test failed login
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        self.login("wronguser", "wrongpass")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_input_trip_details(self):
        """Functionality 3: Input Trip Details"""
        self.login("admin", "admin123")
        
        # Verify trip planner page is displayed with form
        self.assertIn("Trip Planner", self.driver.title)
        self.assertTrue(self.driver.find_element(By.NAME, 'origin').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'destination').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'date').is_displayed())
        
        # Test submitting valid trip details
        self.driver.find_element(By.NAME, 'origin').send_keys('New York')
        self.driver.find_element(By.NAME, 'destination').send_keys('Los Angeles')
        self.driver.find_element(By.NAME, 'date').send_keys('2023-12-25')
        self.driver.find_element(By.XPATH, '//button[text()="Plan Trip"]').click()
        time.sleep(1)
        self.assertIn("Transportation Options", self.driver.page_source)
        
        # Test submitting with empty fields
        self.driver.get('http://localhost:8077/trip')  # Go back to trip page
        self.driver.find_element(By.XPATH, '//button[text()="Plan Trip"]').click()
        time.sleep(1)
        self.assertIn("Missing trip details", self.driver.page_source)

    def test_view_transportation_suggestions(self):
        """Functionality 4: View Transportation Suggestions"""
        self.login("admin", "admin123")
        
        # Input trip details
        self.driver.find_element(By.NAME, 'origin').send_keys('New York')
        self.driver.find_element(By.NAME, 'destination').send_keys('Los Angeles')
        self.driver.find_element(By.NAME, 'date').send_keys('2023-12-25')
        self.driver.find_element(By.XPATH, '//button[text()="Plan Trip"]').click()
        time.sleep(1)
        
        # Verify transportation options are displayed
        options_table = self.driver.find_element(By.TAG_NAME, 'table')
        rows = options_table.find_elements(By.TAG_NAME, 'tr')
        self.assertGreater(len(rows), 1)  # Should have at least one option
        
        # Verify cheapest and fastest options are shown
        self.assertIn("Cheapest:", self.driver.page_source)
        self.assertIn("Fastest:", self.driver.page_source)

    def test_save_preferred_transportation_options(self):
        """Functionality 5: Save Preferred Transportation Options"""
        self.login("admin", "admin123")
        
        # Input trip details
        self.driver.find_element(By.NAME, 'origin').send_keys('New York')
        self.driver.find_element(By.NAME, 'destination').send_keys('Los Angeles')
        self.driver.find_element(By.NAME, 'date').send_keys('2023-12-25')
        self.driver.find_element(By.XPATH, '//button[text()="Plan Trip"]').click()
        time.sleep(1)
        
        # Click save trip button
        self.driver.find_element(By.XPATH, '//button[text()="Save Trip"]').click()
        time.sleep(1)
        self.assertIn("Trip saved successfully", self.driver.page_source)

    def test_user_logout(self):
        """Functionality 6: User Logout"""
        self.login("admin", "admin123")
        
        # Click logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)
        
        # Try to access trip page after logout
        self.driver.get('http://localhost:8077/trip')
        time.sleep(1)
        self.assertIn("Login", self.driver.title)  # Should redirect to login

    def test_view_estimated_costs_and_travel_times(self):
        """Functionality 7: View Estimated Costs and Travel Times"""
        self.login("admin", "admin123")
        
        # Input trip details
        self.driver.find_element(By.NAME, 'origin').send_keys('New York')
        self.driver.find_element(By.NAME, 'destination').send_keys('Los Angeles')
        self.driver.find_element(By.NAME, 'date').send_keys('2023-12-25')
        self.driver.find_element(By.XPATH, '//button[text()="Plan Trip"]').click()
        time.sleep(1)
        
        # Verify costs and times are displayed
        options_table = self.driver.find_element(By.TAG_NAME, 'table')
        rows = options_table.find_elements(By.TAG_NAME, 'tr')
        for row in rows[1:]:  # Skip header row
            cells = row.find_elements(By.TAG_NAME, 'td')
            self.assertEqual(len(cells), 3)  # Type, Cost, Duration
            self.assertTrue('$' in cells[1].text)  # Cost should have dollar sign

    def test_compare_transportation_options(self):
        """Functionality 8: Compare Transportation Options"""
        self.login("admin", "admin123")
        
        # Input trip details
        self.driver.find_element(By.NAME, 'origin').send_keys('New York')
        self.driver.find_element(By.NAME, 'destination').send_keys('Los Angeles')
        self.driver.find_element(By.NAME, 'date').send_keys('2023-12-25')
        self.driver.find_element(By.XPATH, '//button[text()="Plan Trip"]').click()
        time.sleep(1)
        
        # Verify comparison is shown
        self.assertIn("Cheapest:", self.driver.page_source)
        self.assertIn("Fastest:", self.driver.page_source)
        
        # Get all options for manual comparison
        options_table = self.driver.find_element(By.TAG_NAME, 'table')
        options = []
        rows = options_table.find_elements(By.TAG_NAME, 'tr')[1:]  # Skip header
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            options.append({
                'type': cells[0].text,
                'cost': float(cells[1].text.replace('$', '')),
                'duration': cells[2].text
            })
        
        # Verify cheapest and fastest are correctly identified
        cheapest = min(options, key=lambda x: x['cost'])
        fastest = min(options, key=lambda x: x['duration'])
        
        self.assertIn(cheapest['type'], self.driver.page_source)
        self.assertIn(fastest['type'], self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
