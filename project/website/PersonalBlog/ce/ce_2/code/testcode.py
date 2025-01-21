import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestPersonalBlogApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8976/')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Functionalities 1: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys('newuser')
        self.driver.find_element(By.NAME, 'password').send_keys('newpassword')
        self.driver.find_element(By.NAME, 'email').send_keys('newuser@example.com')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Functionalities 2: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Main Blog Page has loaded
        self.assertIn("Main Blog", self.driver.title)

    def test_create_new_blog_post(self):
        # Functionalities 3: Test creating a new blog post
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Post').click()
        self.driver.find_element(By.NAME, 'title').send_keys('New Post Title')
        self.driver.find_element(By.NAME, 'content').send_keys('This is the content of the new post.')
        self.driver.find_element(By.XPATH, '//button[text()="Create Post"]').click()

        # Verify that the new post is displayed on the Main Blog Page
        self.assertIn('New Post Title', self.driver.page_source)

    def test_view_blog_posts(self):
        # Functionalities 4: Test viewing blog posts after logging in
        self.login("admin", "admin123")

        # Verify that the Main Blog Page shows posts
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No blog posts found.")

    def test_edit_existing_post(self):
        # Functionalities 5: Test editing an existing post
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'First Post').click()
        self.driver.find_element(By.LINK_TEXT, 'Edit Post').click()
        self.driver.find_element(By.NAME, 'title').clear()
        self.driver.find_element(By.NAME, 'title').send_keys('Updated Post Title')
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.NAME, 'content').send_keys('Updated content of the post.')
        self.driver.find_element(By.XPATH, '//button[text()="Update Post"]').click()

        # Verify that the post is updated on the Main Blog Page
        self.assertIn('Updated Post Title', self.driver.page_source)

    def test_delete_blog_post(self):
        # Functionalities 6: Test deleting a blog post
        self.fail("Delete functionality not implemented in the codebase")

    def test_navigation(self):
        # Functionalities 7: Test navigation from View Post Page to Main Blog Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'First Post').click()
        self.driver.find_element(By.LINK_TEXT, 'Back to Main').click()

        # Verify that the user is returned to the Main Blog Page
        self.assertIn("Main Blog", self.driver.title)

    def test_user_logout(self):
        # Functionalities 8: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
