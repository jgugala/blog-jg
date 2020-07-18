from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True, )
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    # or define `get_success_url` method in the correspondent class based view
    # def get_absolute_url(self):
    #     return reverse('post_details', args=[self.object.slug])


class PostPhoto(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='images/',  blank=True, null=True)
    # photo = models.ImageField(upload_to=user_directory_path)
