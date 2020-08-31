from django.contrib.auth.models import User
from django.test import TestCase

from ..forms import PostAddForm


class PostCreateFormTest(TestCase):

    def test_title_field_label(self):
        # GIVEN
        form = PostAddForm()
        expected_title_label = 'Title'
        # WHEN
        actual_title_label = form.fields['title'].label
        # THEN
        self.assertEquals(expected_title_label, actual_title_label)

    def test_title_field_help_text(self):
        # GIVEN
        form = PostAddForm()
        expected_title_help_text = ''
        # WHEN
        actual_title_help_text = form.fields['title'].help_text
        # THEN
        self.assertEquals(expected_title_help_text, actual_title_help_text)

    def test_slug_field_label(self):
        # GIVEN
        form = PostAddForm()
        expected_slug_label = 'Slug'
        # WHEN
        actual_slug_label = form.fields['slug'].label
        # THEN
        self.assertEquals(expected_slug_label, actual_slug_label)

    def test_author_field_label(self):
        # GIVEN
        form = PostAddForm()
        expected_author_label = 'Author'
        # WHEN
        actual_author_label = form.fields['author'].label
        # THEN
        self.assertEquals(expected_author_label, actual_author_label)

    def test_content_field_label(self):
        # GIVEN
        form = PostAddForm()
        expected_content_label = 'Content'
        # WHEN
        actual_content_label = form.fields['content'].label
        # THEN
        self.assertEquals(expected_content_label, actual_content_label)

    def test_status_field_label(self):
        # GIVEN
        form = PostAddForm()
        expected_status_label = 'Status'
        # WHEN
        actual_status_label = form.fields['status'].label
        # THEN
        self.assertEquals(expected_status_label, actual_status_label)

    def test_invalid_form(self):
        # GIVEN
        data = {'title': '', 'slug': '', 'author': None, 'content': '', 'status': 0}
        # WHEN
        form = PostAddForm(data=data)
        # THEN
        self.assertFalse(form.is_valid())

    def test_valid_form(self):
        # GIVEN
        user = User.objects.create_user(username='test-user', password='121345')
        data = {'title': 'My test post', 'slug': 'my-test-post', 'author': user, 'content': 'Test content', 'status': 0}
        # WHEN
        form = PostAddForm(data=data)
        # THEN
        self.assertTrue(form.is_valid())
