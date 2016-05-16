#import datetime
from django.db                              import models
from django.utils                           import timezone
#from django.contrib.auth.models             import User
from users.models                           import Person

class E(models.Model):
  author                  = models.ForeignKey('auth.User', related_name="author")
  e_date                  = models.DateField('Date of the event, in the format "yyyy-mm-dd", e.g. for 31st December 2015, enter "2015-12-31"', default=timezone.now, blank=True,null=True)
  detail_public           = models.CharField('Title of event, this be shown publicly', max_length= 80, blank=True,null=True)
  detail_private          = models.TextField('Details of event', blank=True,null=True)
  #detail_private          = models.CharField('Details of event', max_length= 1000, blank=True,null=True)
  notes                   = models.TextField(blank=True,null=True)
  attendees               = models.ManyToManyField(Person, related_name="bookedin", blank=True)
  created_date            = models.DateTimeField(default=timezone.now)
  is_live                 = models.BooleanField(default=True)
  def __str__(self):
    return self.detail_public





