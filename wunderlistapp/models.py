from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Folder(models.Model):
		name = models.CharField(max_length=100, blank=True, default='')
		description = models.TextField(blank=True, default='')
		end = models.DateField(unique=True)
		def __unicode__(self):
			return self.name or _('Folder ending %s') % self.end


class Task(models.Model):
		STATUS_TODO = 1
		STATUS_IN_PROGRESS = 2
		STATUS_DONE = 3
		STATUS_CHOICES = (
			(STATUS_TODO, _('Not Started')),
			(STATUS_IN_PROGRESS, _('In Progress')),
			(STATUS_DONE, _('Done')),
			)
		name = models.CharField(max_length=100)
		description = models.TextField(blank=True, default='')
		folder = models.ForeignKey(Folder, blank=True, null=True)
		status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_TODO)
		order = models.SmallIntegerField(default=0)
		assigned = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
		started = models.DateField(blank=True, null=True)
		due = models.DateField(blank=True, null=True)
		completed = models.DateField(blank=True, null=True)
		def __unicode__(self):
			return self.name