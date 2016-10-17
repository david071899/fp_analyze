from __future__ import unicode_literals

from django.db import models

# from fp_analyze.text_mining.models import Term

from jsonfield import JSONField

class Post (models.Model):
  post_id = models.CharField(max_length = 255)
  content = models.TextField()
  release_time = models.DateTimeField()
  like_count = models.IntegerField(default = 0)
  comment_count = models.IntegerField(default = 0)
  term_frequency = JSONField()
  terms = models.ManyToManyField('text_mining.Term', through = 'TermOfPost')

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

class TermOfPost (models.Model):
  term = models.ForeignKey('text_mining.Term', on_delete = models.CASCADE)
  post = models.ForeignKey(Post, on_delete = models.CASCADE)
  quantity = models.IntegerField(default = 0)
