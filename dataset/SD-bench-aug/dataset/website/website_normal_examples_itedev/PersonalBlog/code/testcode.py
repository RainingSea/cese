import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestPersonalBlogApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the web application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5002')

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
        # Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "test_user"
        new_password = "test_password"
        new_email = "test_user@example.com"

        # Input registration details
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the registration process

        # Verify registration success message
        self.assertIn("Registration successful! Please log in.", self.driver.page_source)

    def test_user_login(self):
        # Test user login functionality
        self.login("user1", "password1")

        # Verify that the main blog page is displayed
        self.assertIn("Welcome to Your Blog, user1", self.driver.page_source)

    def test_create_new_blog_post(self):
        # Test creating a new blog post
        self.login("user1", "password1")

        # Navigate to New Post Page
        self.driver.find_element(By.LINK_TEXT, 'Create New Post').click()
        time.sleep(1)  # Wait for the new post page to load

        post_title = "Test Post"
        post_content = "This is a test post content."

        # Fill out the new post form
        self.driver.find_element(By.NAME, 'title').send_keys(post_title)
        self.driver.find_element(By.NAME, 'content').send_keys(post_content)
        self.driver.find_element(By.XPATH, '//button[text()="Create Post"]').click()
        time.sleep(1)  # Wait for the post creation

        # Verify that the new post is displayed on the main blog page
        self.assertIn(post_title, self.driver.page_source)

    def test_view_blog_posts(self):
        # Test viewing blog posts
        self.login("user1", "password1")

        # Verify that the user's posts are displayed
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No blog posts found.")

    def test_edit_existing_post(self):
        # Test editing an existing post
        self.login("user1", "password1")

        # Navigate to the first post
        self.driver.find_element(By.LINK_TEXT, 'First Post').click()
        time.sleep(1)  # Wait for the post to load

        # Edit the post
        self.driver.find_element(By.LINK_TEXT, 'Edit Post').click()
        time.sleep(1)  # Wait for the edit page to load

        new_title = "Updated First Post"
        new_content = "This is updated content."

        self.driver.find_element(By.NAME, 'title').clear()
        self.driver.find_element(By.NAME, 'title').send_keys(new_title)
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.NAME, 'content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Update Post"]').click()
        time.sleep(1)  # Wait for the update

        # Verify the post is updated
        self.assertIn("Post updated successfully!", self.driver.page_source)

    def test_delete_blog_post(self):
        # Test deleting a blog post
        self.login("user1", "password1")

        # Delete the first post
        self.driver.find_element(By.XPATH, '//li//button[text()="Delete"]').click()
        time.sleep(1)  # Wait for the deletion

        # Verify the post is deleted
        self.assertIn("Post deleted successfully!", self.driver.page_source)

    def test_navigation(self):
        # Test navigation from view post page to main blog page
        self.login("user1", "password1")

        # Navigate to the first post
        self.driver.find_element(By.LINK_TEXT, 'First Post').click()
        time.sleep(1)  # Wait for the post to load

        # Navigate back to main blog page
        self.driver.find_element(By.LINK_TEXT, 'Back to Main Blog').click()
        time.sleep(1)  # Wait for the main blog page to load

        # Verify the main blog page is displayed
        self.assertIn("Welcome to Your Blog, user1", self.driver.page_source)

    def test_user_logout(self):
        # Test user logout functionality
        self.login("user1", "password1")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the logout process

        # Verify that the login page is displayed
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
