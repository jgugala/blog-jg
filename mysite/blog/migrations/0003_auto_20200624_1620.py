# Generated by Django 3.0.6 on 2020-06-24 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='photo',
        ),
        migrations.CreateModel(
            name='PostPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='blog.Post')),
            ],
        ),
    ]
