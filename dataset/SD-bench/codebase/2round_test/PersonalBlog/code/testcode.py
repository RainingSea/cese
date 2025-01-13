import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestPersonalBlogApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8074')

    def tearDown(self):
        # Close the web driver session and terminate the web application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "testuser"
        new_password = "testpass"
        new_email = "testuser@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "adminpass")

        # Verify that the main blog page has loaded
        self.assertIn("Welcome to the Blog", self.driver.page_source)

    def test_create_new_blog_post(self):
        # Test creating a new blog post
        self.login("admin", "adminpass")

        # Navigate to Create New Post Page
        self.driver.find_element(By.LINK_TEXT, 'Create New Post').click()
        time.sleep(1)  # Wait for the new post page to load

        post_title = "Test Post"
        post_content = "This is a test post content."

        # Fill out the new post form
        self.driver.find_element(By.NAME, 'title').send_keys(post_title)
        self.driver.find_element(By.NAME, 'content').send_keys(post_content)
        self.driver.find_element(By.XPATH, '//button[text()="Create Post"]').click()
        time.sleep(1)  # Wait for the post to be created

        # Verify that the new post is displayed on the main page
        self.assertIn(post_title, self.driver.page_source)

    def test_view_blog_posts(self):
        # Test viewing blog posts after logging in
        self.login("admin", "adminpass")

        # Verify that the main blog page shows posts
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No blog posts found.")

    def test_edit_existing_post(self):
        # Test editing an existing post
        self.login("admin", "adminpass")

        # Navigate to Edit Post Page
        self.driver.find_element(By.LINK_TEXT, 'Edit').click()
        time.sleep(1)  # Wait for the edit post page to load

        new_content = "Updated content for the test post."

        # Update the post content
        content_field = self.driver.find_element(By.NAME, 'content')
        content_field.clear()
        content_field.send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Update Post"]').click()
        time.sleep(1)  # Wait for the post to be updated

        # Verify that the updated post is displayed on the main page
        self.assertIn(new_content, self.driver.page_source)

    def test_delete_blog_post(self):
        # Test deleting a blog post
        self.login("admin", "adminpass")

        # Delete the first post
        self.driver.find_element(By.XPATH, '//form/button[text()="Delete"]').click()
        time.sleep(1)  # Wait for the post to be deleted

        # Verify that the post is no longer displayed on the main page
        self.assertNotIn("First Post", self.driver.page_source)

    def test_navigation(self):
        # Test navigation from View Post Page to Main Blog Page
        self.login("admin", "adminpass")

        # View a post
        self.driver.find_element(By.LINK_TEXT, 'View').click()
        time.sleep(1)  # Wait for the view post page to load

        # Navigate back to the main page
        self.driver.find_element(By.LINK_TEXT, 'Back to Main').click()
        time.sleep(1)  # Wait for the main page to load

        # Verify that the main blog page has loaded
        self.assertIn("Welcome to the Blog", self.driver.page_source)

    def test_user_logout(self):
        # Test logging out
        self.login("admin", "adminpass")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the login page to load

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
