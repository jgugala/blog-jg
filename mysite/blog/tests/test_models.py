from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.test import TestCase

from ..models import Post


class PostModelTest(TestCase):

    # is called once at the beginning of the test run for class-level setup.
    # You'd use this to create objects that aren't going to be modified or changed in any of the test methods.
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test-user', password='121345')
        Post.objects.create(title='My test post', slug='my-test-post', author=user)

    #  is called before every test function to set up any objects that may be modified by the test
    #  (every test function will get a "fresh" version of these objects).
    def setUp(self) -> None:
        pass

    def test_title_label(self):
        # GIVEN
        post = get_object_or_404(Post, pk=1)
        expected_title_label = 'title'
        # WHEN
        actual_title_label = post._meta.get_field('title').verbose_name
        # THEN
        self.assertEquals(expected_title_label, actual_title_label)

    def test_title_max_length(self):
        # GIVEN
        post = get_object_or_404(Post, pk=1)
        expected_title_max_length = 200
        # WHEN
        actual_title_max_length = post._meta.get_field('title').max_length
        # THEN
        self.assertEqual(expected_title_max_length, actual_title_max_length)

    def test_slug_max_length(self):
        # GIVEN
        post = get_object_or_404(Post, pk=1)
        expected_slug_max_length = 200
        # WHEN
        actual_slug_max_length = post._meta.get_field('title').max_length
        # THEN
        self.assertEqual(expected_slug_max_length, actual_slug_max_length)

    def test_str(self):
        # GIVEN
        post = get_object_or_404(Post, pk=1)
        expected_str = 'My test post'
        # WHEN
        actual_str = str(post)
        # THEN
        self.assertEqual(expected_str, actual_str)

    def test_get_absolute_url(self):
        # GIVEN
        post = get_object_or_404(Post, pk=1)
        expected_url = '/my-test-post/'
        # WHEN
        actual_url = post.get_absolute_url()
        # THEN
        self.assertEqual(expected_url, actual_url)

    def tearDown(self) -> None:
        pass
