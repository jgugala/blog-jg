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

    def test_list_all_posts_for_admin(self):
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

    def test_exception_for_non_admin_user_and_draft_post(self):
        # WHEN
        response = self.client.get('/my-test-post1/')
        # THEN
        self.assertEquals(response.status_code, 403)

