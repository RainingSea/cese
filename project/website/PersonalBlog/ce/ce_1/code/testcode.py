import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestPersonalBlogApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8187/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Functionalities 1: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        self.driver.find_element(By.NAME, 'username').send_keys('testuser')
        self.driver.find_element(By.NAME, 'password').send_keys('testpassword')
        self.driver.find_element(By.NAME, 'email').send_keys('testuser@example.com')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the redirection to login page

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Functionalities 2: User Login
        self.login("user1", "password1")

        # Verify that the Main Blog Page has loaded
        self.assertIn("Main Blog", self.driver.title)

    def test_create_new_blog_post(self):
        # Functionalities 3: Create a New Blog Post
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Create New Post').click()
        time.sleep(1)  # Wait for the new post page to load

        self.driver.find_element(By.NAME, 'title').send_keys('Test Post')
        self.driver.find_element(By.NAME, 'content').send_keys('This is a test post content.')
        self.driver.find_element(By.XPATH, '//button[text()="Create Post"]').click()
        time.sleep(1)  # Wait for the redirection to main page

        # Verify that the new post is displayed on the Main Blog Page
        self.assertIn('Test Post', self.driver.page_source)

    def test_view_blog_posts(self):
        # Functionalities 4: View Blog Posts
        self.login("user1", "password1")

        # Verify that the Main Blog Page shows posts
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No blog posts found.")

    def test_edit_existing_post(self):
        # Functionalities 5: Edit an Existing Post
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'First Post').click()
        time.sleep(1)  # Wait for the view post page to load

        self.driver.find_element(By.LINK_TEXT, 'Edit').click()
        time.sleep(1)  # Wait for the edit post page to load

        self.driver.find_element(By.NAME, 'title').clear()
        self.driver.find_element(By.NAME, 'title').send_keys('Updated First Post')
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.NAME, 'content').send_keys('Updated content of the first post.')
        self.driver.find_element(By.XPATH, '//button[text()="Update Post"]').click()
        time.sleep(1)  # Wait for the redirection to main page

        # Verify that the updated post is displayed on the Main Blog Page
        self.assertIn('Updated First Post', self.driver.page_source)

    def test_delete_blog_post(self):
        # Functionalities 6: Delete a Blog Post
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'First Post').click()
        time.sleep(1)  # Wait for the view post page to load

        self.driver.find_element(By.LINK_TEXT, 'Delete').click()
        time.sleep(1)  # Wait for the redirection to main page

        # Verify that the post is no longer displayed on the Main Blog Page
        self.assertNotIn('First Post', self.driver.page_source)

    def test_navigation(self):
        # Functionalities 7: Navigation
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'First Post').click()
        time.sleep(1)  # Wait for the view post page to load

        self.driver.find_element(By.LINK_TEXT, 'Back to Main').click()
        time.sleep(1)  # Wait for the redirection to main page

        # Verify that the Main Blog Page has loaded
        self.assertIn("Main Blog", self.driver.title)

    def test_user_logout(self):
        # Functionalities 8: User Logout
        self.login("user1", "password1")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the redirection to login page

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
