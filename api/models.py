from __future__ import unicode_literals

from django.db import models

from jsonfield import JSONField

class Wordcloud (models.Model):
  year = models.IntegerField(default = 2014)
  month = models.IntegerField(default = 1)
  school = models.CharField(max_length = 255)
  word_data = JSONField()