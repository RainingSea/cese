import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestPersonalBlogApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8548')

    def tearDown(self):
        # Close the web driver session and stop the web application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Functionalities 1: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        self.driver.find_element(By.ID, 'username').send_keys('newuser')
        self.driver.find_element(By.ID, 'password').send_keys('newpassword')
        self.driver.find_element(By.ID, 'email').send_keys('newuser@example.com')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Functionalities 2: User Login
        self.login("admin", "admin123")

        # Verify that the main blog page is displayed
        self.assertIn("Main Blog", self.driver.title)

    def test_create_new_blog_post(self):
        # Functionalities 3: Create a New Blog Post
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'New Post').click()
        time.sleep(1)  # Wait for the new post page to load

        self.driver.find_element(By.ID, 'title').send_keys('Test Post')
        self.driver.find_element(By.ID, 'content').send_keys('This is a test post.')
        self.driver.find_element(By.XPATH, '//button[text()="Create Post"]').click()
        time.sleep(1)  # Wait for the main page to load

        # Verify that the new post is displayed on the main page
        self.assertIn('Test Post', self.driver.page_source)

    def test_view_blog_posts(self):
        # Functionalities 4: View Blog Posts
        self.login("admin", "admin123")

        # Verify that the main blog page shows posts
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No blog posts found.")

    def test_edit_existing_post(self):
        # Functionalities 5: Edit an Existing Post
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'First Post').click()
        time.sleep(1)  # Wait for the view post page to load

        self.driver.find_element(By.LINK_TEXT, 'Edit Post').click()
        time.sleep(1)  # Wait for the edit post page to load

        self.driver.find_element(By.ID, 'title').clear()
        self.driver.find_element(By.ID, 'title').send_keys('Updated First Post')
        self.driver.find_element(By.ID, 'content').clear()
        self.driver.find_element(By.ID, 'content').send_keys('Updated content.')
        self.driver.find_element(By.XPATH, '//button[text()="Update Post"]').click()
        time.sleep(1)  # Wait for the main page to load

        # Verify that the updated post is displayed on the main page
        self.assertIn('Updated First Post', self.driver.page_source)

    def test_delete_blog_post(self):
        # Functionalities 6: Delete a Blog Post
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Second Post').click()
        time.sleep(1)  # Wait for the view post page to load

        self.driver.find_element(By.XPATH, '//button[text()="Delete Post"]').click()
        time.sleep(1)  # Wait for the main page to load

        # Verify that the post is no longer displayed on the main page
        self.assertNotIn('Second Post', self.driver.page_source)

    def test_navigation(self):
        # Functionalities 7: Navigation
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'First Post').click()
        time.sleep(1)  # Wait for the view post page to load

        self.driver.find_element(By.LINK_TEXT, 'Back to Main').click()
        time.sleep(1)  # Wait for the main page to load

        # Verify that the main blog page is displayed
        self.assertIn("Main Blog", self.driver.title)

    def test_user_logout(self):
        # Functionalities 8: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the login page to load

        # Verify that the login page is displayed
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
