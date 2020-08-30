"""
This is my worthless test.
>>> print("wee")
wee
>>> print(False)
False


Go to the home and create post (allowed only with superuser permissions) pages, check statuses.
Next try to create a sample post, save it and go to its details page.
At the end go back to the home and check the context value for posts list.
>>> from django.test import Client
>>> from django.contrib.auth.models import User
>>> import datetime
>>> from blog.models import Post

>>> from django.urls import reverse
>>> client = Client()
>>> password='12345'
>>> user = User.objects.create_superuser(username='test-user', password=password)
>>> client.login(username=user.username, password=password)
True

>>> response = client.get(reverse('home'))
>>> response.status_code
200

>>> response = client.get(reverse('post_create'))
>>> response.status_code
200

>>> post = Post(title='My post', slug='my-post', content='Lorem ipsum dolor sit amet', status=1, author=user, \
created_on=datetime.datetime(2008,5,5,16,20))
>>> post.save()

>>> response = client.get(post.get_absolute_url())
>>> response.status_code
200
>>> response.context['post']
<Post: My post>


>>> response = client.get(reverse('home'))
>>> response.context['posts'][0]
<Post: My post>

>>> User.objects.get(pk=user.pk).delete()
(2, {'admin.LogEntry': 0, 'auth.User_groups': 0, 'auth.User_user_permissions': 0, 'blog.PostPhoto': 0, 'blog.Post': 1, 'auth.User': 1})
"""
