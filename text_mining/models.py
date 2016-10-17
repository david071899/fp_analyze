from __future__ import unicode_literals
from django.db import models

from data_parser.models import Post, User, Comment

class Term (models.Model):
  value = models.CharField(max_length = 255)
  frequency_of_all_post = models.IntegerField(default = 0)
  related_term = models.ManyToManyField('self')





