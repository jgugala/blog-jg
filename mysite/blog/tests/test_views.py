from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse

from ..models import Post


class PostsListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_published_posts = 5
        number_of_draft_posts = 3
        user = User.objects.create_user(username='test-user', password='121345')

        for post_id in range(number_of_published_posts):
            Post.objects.create(title=f'My test post{post_id}', slug=f'my-test-post{post_id}', author=user, status=1)

        for post_id in range(number_of_published_posts, number_of_published_posts + number_of_draft_posts):
            Post.objects.create(title=f'My test post{post_id}', slug=f'my-test-post{post_id}', author=user, status=0)

    def test_view_url_exists_at_desired_location(self):
        # WHEN
        response = self.client.get('/')
        # THEN
        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        # WHEN
        response = self.client.get(reverse('home'))
        # THEN
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        # WHEN
        response = self.client.get(reverse('home'))
        # THEN
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_list_all_posts(self):
        # GIVEN
        expected_posts_list_size = 5
        # WHEN
        response = self.client.get(reverse('home'))
        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(response.context['posts']), expected_posts_list_size)

    def test_list_searched_posts(self):
        # GIVEN
        expected_posts_list_size = 1
        # WHEN
        response = self.client.get(reverse('search_results'), {'q': 'My test post4'})
        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(response.context['posts']), expected_posts_list_size)

    def test_list_all_posts_for_superuser(self):
        # GIVEN
        expected_posts_list_size = 8
        password = '12345-super'
        superuser = User.objects.create_superuser(username='test-user-super', password=password)
        self.client.login(username=superuser.username, password=password)
        # WHEN
        response = self.client.get(reverse('home'))
        # THEN
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'test-user-super')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(response.context['posts']), expected_posts_list_size)


class PostDetailsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test-user', password='121345')
        Post.objects.create(title='My test post1', slug='my-test-post1', author=user, status=0)
        Post.objects.create(title='My test post2', slug='my-test-post2', author=user, status=1)

    def test_view_url_exists_at_desired_location(self):
        # WHEN
        response = self.client.get('/my-test-post2/')
        # THEN
        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        # WHEN
        response = self.client.get(reverse('post_details', kwargs={'slug': 'my-test-post2'}))
        # THEN
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        # WHEN
        response = self.client.get(reverse('post_details', kwargs={'slug': 'my-test-post2'}))
        # THEN
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_details.html')

    def test_exception_for_non_superuser_and_draft_post(self):
        # WHEN
        response = self.client.get('/my-test-post1/')
        # THEN
        self.assertEquals(response.status_code, 403)


class PostCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username='test-user-super', password='12345-super')

    def test_view_url_accessible_for_superuser(self):
        # GIVEN
        self.client.login(username='test-user-super', password='12345-super')
        # WHEN
        response = self.client.get(reverse('post_create'))
        # THEN
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        # GIVEN
        self.client.login(username='test-user-super', password='12345-super')
        # WHEN
        response = self.client.get(reverse('post_create'))
        # THEN
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_add.html')

    def test_view_url_not_accessible_for_standard_user(self):
        # GIVEN
        User.objects.create_user(username='test-user', password='12345')
        self.client.login(username='test-user', password='12345')
        # WHEN
        response = self.client.get(reverse('post_create'))
        # THEN
        self.assertEquals(response.status_code, 403)

    def test_view_url_redirect_for_not_logged_in_user(self):
        # WHEN
        response = self.client.get(reverse('post_create'))
        # THEN
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/sign-in?next=/create/', target_status_code=301)


class SignInViewTest(TestCase):

    def test_view_accessible_for_not_logged_in_user(self):
        # WHEN
        response = self.client.get(reverse('sign_in'))
        # THEN
        self.assertEquals(response.status_code, 200)

    def test_view_redirect_to_home_for_already_logged_in_user(self):
        # GIVEN
        User.objects.create_user(username='test-user', password='12345')
        self.client.login(username='test-user', password='12345')
        # WHEN
        response = self.client.get(reverse('sign_in'))
        # THEN
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_user_sign_in_and_redirect_to_home(self):
        # GIVEN
        User.objects.create_user(username='test-user', password='12345')
        # WHEN
        response = self.client.post(reverse('sign_in'), {'username': 'test-user', 'password': '12345'}, follow=True)
        # THEN
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertEquals(response.redirect_chain[-1][-1], 302)
        self.assertRedirects(response, '/')
