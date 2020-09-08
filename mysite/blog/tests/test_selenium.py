
import time

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class CreatePostTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)

    def setUp(self) -> None:
        User.objects.create_superuser(username='test-user-super', password='12345-super')

    def test_sign_in_as_superuser_and_create_post(self):
        # got to the login page and sign in
        self.driver.get('%s%s' % (self.live_server_url, '/sign-in/'))
        username_input = self.driver.find_element_by_id("id_username")
        username_input.send_keys('test-user-super')
        password_input = self.driver.find_element_by_id("id_password")
        password_input.send_keys('12345-super')
        self.driver.find_element_by_class_name('login100-form-btn').click()

        # go to the post creation form, fill it in and create a new post
        self.driver.find_element_by_link_text("CREATE NEW POST").click()
        post_title_input = self.driver.find_element_by_id("id_title")
        post_title_input.send_keys('My test post')
        post_author_selector = self.driver.find_element_by_id("id_author")
        post_author_selector.send_keys('test-user-super')
        post_content_input = self.driver.find_element_by_id("id_content")
        post_content_input.send_keys('My test post content')
        self.driver.find_element_by_class_name('btn.btn-primary').click()

        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


class DeletePostTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)

    def setUp(self) -> None:
        User.objects.create_superuser(username='test-user-super', password='12345-super')

    def test_create_post_go_to_home_and_delete_it(self):
        # got to the login page and sign in
        self.driver.get('%s%s' % (self.live_server_url, '/sign-in/'))
        username_input = self.driver.find_element_by_id("id_username")
        username_input.send_keys('test-user-super')
        password_input = self.driver.find_element_by_id("id_password")
        password_input.send_keys('12345-super')
        self.driver.find_element_by_class_name('login100-form-btn').click()

        # go to the post creation form, fill it in and create a new post
        self.driver.find_element_by_link_text("CREATE NEW POST").click()
        post_title_input = self.driver.find_element_by_id("id_title")
        post_title_input.send_keys('My test post')
        post_author_selector = self.driver.find_element_by_id("id_author")
        post_author_selector.send_keys('test-user-super')
        post_content_input = self.driver.find_element_by_id("id_content")
        post_content_input.send_keys('My test post content')
        self.driver.find_element_by_class_name('btn.btn-primary').click()

        # back to the home page and delete a newly created post
        # this doesn't work, time.sleep() used instead:
        # WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'fas.fa-home'))).click()
        time.sleep(0.5)
        self.driver.find_element_by_class_name('fas.fa-home').click()
        self.driver.find_element_by_class_name('fa.fa-trash-alt').click()
        self.driver.find_element_by_class_name('btn.btn-primary.confirm-post-delete').click()

        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
