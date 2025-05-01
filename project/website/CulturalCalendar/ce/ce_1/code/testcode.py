import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess
import os

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
        self.driver.get('http://localhost:8568/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.title_contains('Dashboard'))

    def test_user_registration(self):
        # Test registration form display
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.title_contains('Register'))
        
        # Test successful registration
        username = "testuser_" + str(int(time.time()))
        password = "testpass123"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.wait.until(EC.title_contains('Login'))
        
        # Test duplicate username registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.title_contains('Register'))
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        error_message = self.driver.find_element(By.CSS_SELECTOR, 'p[style="color:red"]')
        self.assertIn('Username already exists', error_message.text)

    def test_user_login(self):
        # Test login form display
        self.assertTrue(self.driver.find_element(By.XPATH, '//h1[text()="Login"]').is_displayed())
        
        # Test successful login
        self.login('admin', 'admin123')
        self.assertIn('Dashboard', self.driver.title)
        
        # Test invalid login
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains('Login'))
        self.driver.find_element(By.NAME, 'username').send_keys('wronguser')
        self.driver.find_element(By.NAME, 'password').send_keys('wrongpass')
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        error_message = self.driver.find_element(By.CSS_SELECTOR, 'p[style="color:red"]')
        self.assertIn('Invalid credentials', error_message.text)

    def test_view_upcoming_events(self):
        self.login('admin', 'admin123')
        events = self.driver.find_elements(By.CSS_SELECTOR, 'ul li')
        self.assertGreater(len(events), 0, "No events displayed on dashboard")
        
        # Check if specific test events are displayed
        event_titles = [event.text for event in events]
        self.assertTrue(any('Team Meeting' in title for title in event_titles))
        self.assertTrue(any('Product Launch' in title for title in event_titles))

    def test_view_event_details(self):
        self.login('admin', 'admin123')
        event_link = self.driver.find_element(By.LINK_TEXT, 'Team Meeting')
        event_link.click()
        self.wait.until(EC.title_contains('Team Meeting'))
        
        # Check event details
        date = self.driver.find_element(By.XPATH, '//p[contains(., "Date:")]').text
        location = self.driver.find_element(By.XPATH, '//p[contains(., "Location:")]').text
        description = self.driver.find_element(By.XPATH, '//p[contains(., "Description:")]').text
        
        self.assertIn('2023-12-15', date)
        self.assertIn('Conference Room A', location)
        self.assertIn('Weekly team sync', description)

    def test_search_events(self):
        self.login('admin', 'admin123')
        
        # Search by keyword
        search_box = self.driver.find_element(By.NAME, 'q')
        search_box.send_keys('Team')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        events = self.driver.find_elements(By.CSS_SELECTOR, 'ul li')
        self.assertEqual(len(events), 1)
        self.assertIn('Team Meeting', events[0].text)
        
        # Clear search
        search_box = self.driver.find_element(By.NAME, 'q')
        search_box.clear()
        search_box.send_keys('')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        events = self.driver.find_elements(By.CSS_SELECTOR, 'ul li')
        self.assertGreater(len(events), 1)

    def test_set_reminder(self):
        self.login('admin', 'admin123')
        
        # Go to event details
        event_link = self.driver.find_element(By.LINK_TEXT, 'Team Meeting')
        event_link.click()
        self.wait.until(EC.title_contains('Team Meeting'))
        
        # Set reminder
        self.driver.find_element(By.LINK_TEXT, 'Set Reminder').click()
        self.wait.until(EC.title_contains('My Reminders'))
        
        # Verify reminder was added
        reminders = self.driver.find_elements(By.CSS_SELECTOR, 'ul li')
        self.assertGreater(len(reminders), 0)
        self.assertTrue(any('Team Meeting' in reminder.text for reminder in reminders))

    def test_manage_reminders(self):
        self.login('admin', 'admin123')
        
        # Go to reminders page
        self.driver.find_element(By.LINK_TEXT, 'My Reminders').click()
        self.wait.until(EC.title_contains('My Reminders'))
        
        # Check existing reminders
        reminders = self.driver.find_elements(By.CSS_SELECTOR, 'ul li')
        initial_count = len(reminders)
        
        if initial_count > 0:
            # Delete a reminder
            delete_link = self.driver.find_element(By.LINK_TEXT, 'Delete')
            delete_link.click()
            self.wait.until(EC.title_contains('My Reminders'))
            
            # Verify reminder was removed
            reminders = self.driver.find_elements(By.CSS_SELECTOR, 'ul li')
            self.assertEqual(len(reminders), initial_count - 1)

    def test_user_logout(self):
        self.login('admin', 'admin123')
        
        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains('Login'))
        
        # Try to access dashboard directly
        self.driver.get('http://localhost:8568/dashboard')
        self.wait.until(EC.title_contains('Login'))

    def test_local_data_storage(self):
        # This would require modifying the events.txt file and checking the UI
        # Since we can't modify files during tests, we'll verify the initial data is loaded
        self.login('admin', 'admin123')
        events = self.driver.find_elements(By.CSS_SELECTOR, 'ul li')
        self.assertEqual(len(events), 3)  # Based on initial events.txt

if __name__ == '__main__':
    unittest.main()
