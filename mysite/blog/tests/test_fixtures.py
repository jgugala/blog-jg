from django.test import TestCase
from ..models import Post


class SiteTests(TestCase):
    fixtures = ['blog', 'users']

    def testPostAuthor(self):
        s = Post.objects.get(pk=1)
        self.assertEquals(s.author.username, 'jgugala')
        s.author.username = 'who cares'
        s.save()
