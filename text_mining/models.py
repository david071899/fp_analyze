from __future__ import unicode_literals
from django.db import models

# from fp_analyze.data_parser.models import Post, User, Comment

class Term (models.Model):
  value = models.CharField(max_length = 255)
  frequency_of_all_post = models.IntegerField(default = 0)
  flag = models.CharField(max_length = 255, default = '')
  created_at = models.DateTimeField(default = '2016-11-01 12:00:00+08:00')
  idf = models.FloatField(default = 0)
  related_term = models.ManyToManyField('self')





