import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestPersonalBlogApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8394/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Functionalities 1: User Registration
        self.driver.get('http://localhost:8394/register')  # Navigate to registration page
        self.driver.find_element(By.NAME, 'username').send_keys("testuser")
        self.driver.find_element(By.NAME, 'password').send_keys("testpassword")
        self.driver.find_element(By.NAME, 'email').send_keys("testuser@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Functionalities 2: User Login
        self.login("admin", "admin123")

        # Verify that the main blog page has loaded
        self.assertIn("Your Blog Posts", self.driver.page_source)

    def test_create_new_blog_post(self):
        # Functionalities 3: Create a New Blog Post
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Post').click()

        # Fill out the new post form
        self.driver.find_element(By.NAME, 'title').send_keys("New Blog Post")
        self.driver.find_element(By.NAME, 'content').send_keys("This is the content of the new blog post.")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()

        # Verify that the new post is displayed on the main blog page
        self.assertIn("New Blog Post", self.driver.page_source)

    def test_view_blog_posts(self):
        # Functionalities 4: View Blog Posts
        self.login("admin", "admin123")

        # Verify that the user is presented with their existing blog posts
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No blog posts found.")

    def test_edit_existing_post(self):
        # Functionalities 5: Edit an Existing Post
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "New Blog Post").click()  # Navigate to the new post
        self.driver.find_element(By.LINK_TEXT, "Edit").click()  # Click edit

        # Update the post
        self.driver.find_element(By.NAME, 'title').clear()
        self.driver.find_element(By.NAME, 'title').send_keys("Updated Blog Post")
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.NAME, 'content').send_keys("This is the updated content.")
        self.driver.find_element(By.XPATH, '//button[text()="Update"]').click()

        # Verify that the updated post is displayed
        self.assertIn("Updated Blog Post", self.driver.page_source)

    def test_delete_blog_post(self):
        # Functionalities 6: Delete a Blog Post
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Updated Blog Post").click()  # Navigate to the updated post
        self.driver.find_element(By.XPATH, '//button[text()="Delete"]').click()

        # Verify that the post is no longer displayed
        self.assertNotIn("Updated Blog Post", self.driver.page_source)

    def test_navigate_back_to_main_blog(self):
        # Functionalities 7: Navigation
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "New Blog Post").click()  # Navigate to the new post
        self.driver.find_element(By.LINK_TEXT, "Back to Blog").click()  # Click back

        # Verify that the main blog page is displayed
        self.assertIn("Your Blog Posts", self.driver.page_source)

    def test_user_logout(self):
        # Functionalities 8: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
