from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Post (models.Model):
  post_id = models.CharField(max_length = 255)
  content = models.TextField()
  release_time = models.DateTimeField()
  like_count = models.IntegerField(default = 0)
  comment_count = models.IntegerField(default = 0)

  def __str__(self):
    return self.post_id

class User (models.Model):
  name = models.CharField(max_length = 255)
  user_id = models.CharField(max_length = 255)
  like_post = models.ManyToManyField(Post)
  

  def __str__(self):
    return self.user_id

class Comment (models.Model):
  comment_id = models.CharField(max_length = 255)
  content = models.TextField()
  like_count = models.IntegerField(default = 0)
  user = models.ForeignKey(User)
  post = models.ForeignKey(Post)

  def __str__(self):
    return self.comment_id


