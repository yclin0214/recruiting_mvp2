from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Message(models.Model):
    phone_number = models.CharField(verbose_name='phone number', max_length=11);
    last_update = models.DateTimeField('last update');
    acquired_date = models.DateTimeField('date created');
    text_contents = models.TextField('text contents');
    def __str__(self):
        return self.phone_number + " " + "entry"


