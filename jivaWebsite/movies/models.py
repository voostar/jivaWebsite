from django.db import models
from django.contrib import admin

# Create your models here.
class dy2018_info(models.Model):
	name = models.CharField(max_length=300)
	url = models.CharField(max_length=300, blank=True, null=True)
	hash = models.CharField(max_length=300, blank=True, null=True)
	include_date = models.DateField(auto_now=False)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ('-include_date',)

class dy2018_links(models.Model):
	hash = models.CharField(max_length=300)
	link = models.CharField(max_length=300, blank=True, null=True)

	def __unicode__(self):
		return self.hash

admin.site.register(dy2018_info)
admin.site.register(dy2018_links)