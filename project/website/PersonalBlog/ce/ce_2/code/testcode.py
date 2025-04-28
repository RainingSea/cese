import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestPersonalBlogApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the actual port from main.py

    def tearDown(self):
        # Close the web driver session and terminate the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:5000/login')  # Navigate to login page
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_registration(self):
        # Functionalities 1: User Registration
        self.driver.get('http://localhost:5000/register')  # Navigate to registration page
        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.ID, 'username').send_keys(new_username)
        self.driver.find_element(By.ID, 'password').send_keys(new_password)
        self.driver.find_element(By.ID, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_login(self):
        # Functionalities 2: User Login
        self.login("admin", "admin123")

        # Verify that the main blog page has loaded
        self.assertIn("Blog Posts", self.driver.title)

    def test_create_new_post(self):
        # Functionalities 3: Create a New Blog Post
        self.login("admin", "admin123")

        # Navigate to New Post Page
        self.driver.find_element(By.LINK_TEXT, 'Create New Post').click()
        time.sleep(1)  # Wait for the next page to load

        post_title = "My New Blog Post"
        post_content = "This is the content of my new blog post."

        # Fill out the new post form
        self.driver.find_element(By.ID, 'title').send_keys(post_title)
        self.driver.find_element(By.ID, 'content').send_keys(post_content)
        self.driver.find_element(By.XPATH, '//button[text()="Create Post"]').click()
        time.sleep(1)  # Wait for saving the post

        # Verify that the new post is displayed on the main blog page
        self.assertIn(post_title, self.driver.page_source)

    def test_view_blog_posts(self):
        # Functionalities 4: View Blog Posts
        self.login("admin", "admin123")

        # Verify that the main blog page shows posts
        posts = self.driver.find_elements(By.TAG_NAME, 'li')  # Assuming posts are in list items
        self.assertGreater(len(posts), 0, "No blog posts found.")

    def test_edit_post(self):
        # Functionalities 5: Edit an Existing Post
        self.login("admin", "admin123")

        # Navigate to the edit post page (assuming the first post is editable)
        self.driver.find_element(By.LINK_TEXT, 'Edit Post').click()
        time.sleep(1)  # Wait for the next page to load

        new_post_title = "Updated Blog Post"
        new_post_content = "This is the updated content of my blog post."

        # Fill out the edit post form
        self.driver.find_element(By.ID, 'title').clear()
        self.driver.find_element(By.ID, 'title').send_keys(new_post_title)
        self.driver.find_element(By.ID, 'content').clear()
        self.driver.find_element(By.ID, 'content').send_keys(new_post_content)
        self.driver.find_element(By.XPATH, '//button[text()="Update Post"]').click()
        time.sleep(1)  # Wait for updating the post

        # Verify that the updated post is displayed on the main blog page
        self.assertIn(new_post_title, self.driver.page_source)

    def test_delete_post(self):
        # Functionalities 6: Delete a Blog Post
        self.login("admin", "admin123")

        # Assuming we can delete the first post
        self.driver.find_element(By.LINK_TEXT, 'Delete Post').click()
        time.sleep(1)  # Wait for the deletion to process

        # Verify that the post is no longer displayed on the main blog page
        self.assertNotIn("First Post", self.driver.page_source)  # Replace with the actual title of the post

    def test_navigate_back(self):
        # Functionalities 7: Navigation
        self.login("admin", "admin123")

        # Navigate to a post (assuming the first post is viewable)
        self.driver.find_element(By.LINK_TEXT, 'View Post').click()
        time.sleep(1)  # Wait for the next page to load

        # Click the back link
        self.driver.find_element(By.LINK_TEXT, 'Back to Blog').click()
        time.sleep(1)  # Wait for the main blog page to load

        # Verify that the main blog page is displayed
        self.assertIn("Blog Posts", self.driver.title)

    def test_logout(self):
        # Functionalities 8: User Logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
