import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestPersonalBlogApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')  # Replace 5000 with the actual port from main.py

    def tearDown(self):
        # Close the web driver session and the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Functionalities 1: User Registration
        self.driver.get('http://localhost:5000/register')  # Navigate to registration page
        self.driver.find_element(By.NAME, 'username').send_keys("test_user")
        self.driver.find_element(By.NAME, 'password').send_keys("test_password")
        self.driver.find_element(By.NAME, 'email').send_keys("test@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify registration success (assuming it redirects to login page)
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Functionalities 2: User Login
        self.login("admin", "admin123")

        # Verify that the main blog page is displayed
        self.assertIn("Blog Posts", self.driver.title)

    def test_create_new_blog_post(self):
        # Functionalities 3: Create a New Blog Post
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Post').click()

        self.driver.find_element(By.NAME, 'title').send_keys("New Blog Post")
        self.driver.find_element(By.NAME, 'content').send_keys("This is the content of the new blog post.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify the post is created (assuming it redirects to main blog page)
        self.assertIn("Blog Posts", self.driver.title)

    def test_view_blog_posts(self):
        # Functionalities 4: View Blog Posts
        self.login("admin", "admin123")
        
        # Verify that the main blog page shows existing posts
        posts = self.driver.find_elements(By.TAG_NAME, 'li')  # Assuming posts are listed in <li> elements
        self.assertGreater(len(posts), 0, "No blog posts found.")

    def test_edit_existing_post(self):
        # Functionalities 5: Edit an Existing Post
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Edit Post').click()  # Navigate to edit post page

        self.driver.find_element(By.NAME, 'title').clear()
        self.driver.find_element(By.NAME, 'title').send_keys("Updated Blog Post Title")
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.NAME, 'content').send_keys("Updated content for the blog post.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Changes"]').click()

        # Verify the post is updated (assuming it redirects to main blog page)
        self.assertIn("Blog Posts", self.driver.title)

    def test_delete_blog_post(self):
        # Functionalities 6: Delete a Blog Post
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Delete Post').click()  # Assuming there's a delete link

        # Verify the post is deleted (assuming it redirects to main blog page)
        self.assertIn("Blog Posts", self.driver.title)

    def test_navigate_back_to_main_blog(self):
        # Functionalities 7: Navigate back from View Post Page to Main Blog Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Post').click()  # Navigate to view post page
        self.driver.find_element(By.LINK_TEXT, 'Back to Blog').click()  # Navigate back

        # Verify that the main blog page is displayed
        self.assertIn("Blog Posts", self.driver.title)

    def test_user_logout(self):
        # Functionalities 8: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Assuming there's a logout link

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
