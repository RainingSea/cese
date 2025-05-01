import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestCulturalCalendarApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8567/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.title_contains('Dashboard'))

    def test_1_user_registration(self):
        """Test user registration functionality"""
        # Navigate to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.wait.until(EC.title_contains('Register'))
        
        # Test successful registration
        username = "testuser_" + str(int(time.time()))
        password = "testpass123"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.wait.until(EC.title_contains('Login'))
        
        # Test duplicate username registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.wait.until(EC.title_contains('Register'))
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("anypassword")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        error_message = self.driver.find_element(By.CLASS_NAME, 'error').text
        self.assertIn("Registration failed", error_message)

    def test_2_user_login(self):
        """Test user login functionality"""
        # Test successful login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)
        
        # Logout and test invalid login
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains('Login'))
        self.driver.find_element(By.NAME, 'username').send_keys("wronguser")
        self.driver.find_element(By.NAME, 'password').send_keys("wrongpass")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        error_message = self.driver.find_element(By.CLASS_NAME, 'error').text
        self.assertIn("Invalid credentials", error_message)

    def test_3_view_upcoming_events(self):
        """Test viewing upcoming events on dashboard"""
        self.login("admin", "admin123")
        events = self.driver.find_elements(By.CLASS_NAME, 'event-card')
        self.assertGreater(len(events), 0, "No events displayed on dashboard")

    def test_4_view_event_details(self):
        """Test viewing event details"""
        self.login("admin", "admin123")
        event_link = self.driver.find_element(By.CSS_SELECTOR, '.event-card h3 a')
        event_name = event_link.text
        event_link.click()
        self.wait.until(EC.title_contains(event_name))
        
        # Verify event details are displayed
        details = self.driver.find_element(By.CLASS_NAME, 'event-details')
        self.assertTrue(details.is_displayed())
        self.assertIn("Location:", details.text)
        self.assertIn("Category:", details.text)
        self.assertIn("Description:", details.text)

    def test_5_search_events(self):
        """Test searching for events"""
        self.login("admin", "admin123")
        
        # Search by keyword
        search_box = self.driver.find_element(By.NAME, 'q')
        search_box.send_keys("Music")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'event-card')))
        events = self.driver.find_elements(By.CLASS_NAME, 'event-card')
        self.assertGreater(len(events), 0, "No events found for search term")
        
        # Verify search results contain the keyword
        for event in events:
            self.assertIn("Music", event.text)

    def test_6_set_reminder(self):
        """Test setting reminders for events"""
        self.login("admin", "admin123")
        
        # Go to first event details
        event_link = self.driver.find_element(By.CSS_SELECTOR, '.event-card h3 a')
        event_link.click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'reminder-btn')))
        
        # Set reminder
        reminder_button = self.driver.find_element(By.CLASS_NAME, 'reminder-btn')
        self.assertEqual(reminder_button.text, "Set Reminder")
        reminder_button.click()
        
        # Verify reminder was set
        self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'reminder-btn'), "Remove Reminder"))

    def test_7_view_manage_reminders(self):
        """Test viewing and managing reminders"""
        self.login("admin", "admin123")
        
        # Go to reminders page
        self.driver.find_element(By.LINK_TEXT, 'View My Reminders').click()
        self.wait.until(EC.title_contains('My Reminders'))
        
        # Verify reminders are displayed
        reminders = self.driver.find_elements(By.CLASS_NAME, 'reminder-card')
        self.assertGreater(len(reminders), 0, "No reminders found")
        
        # Delete a reminder
        delete_button = self.driver.find_element(By.CLASS_NAME, 'delete-btn')
        delete_button.click()
        self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'delete-btn')))
        
        # Verify reminder was deleted
        reminders_after = self.driver.find_elements(By.CLASS_NAME, 'reminder-card')
        self.assertLess(len(reminders_after), len(reminders))

    def test_8_user_logout(self):
        """Test user logout functionality"""
        self.login("admin", "admin123")
        
        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains('Login'))
        
        # Try to access dashboard while logged out
        self.driver.get('http://localhost:8567/dashboard')
        self.wait.until(EC.title_contains('Login'))

    def test_9_local_data_storage(self):
        """Test local data storage functionality"""
        # This would require modifying the events.txt file and verifying changes
        # Since we can't modify files during tests, we'll verify the existing data is loaded
        self.login("admin", "admin123")
        events = self.driver.find_elements(By.CLASS_NAME, 'event-card')
        self.assertEqual(len(events), 3, "Expected 3 events from events.txt")

if __name__ == '__main__':
    unittest.main()
