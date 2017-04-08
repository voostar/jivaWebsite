from django.db import models
from django.contrib import admin
# Create your models here.
class house_retal_info(models.Model):
	url = models.CharField(max_length=300)
	name = models.CharField(max_length=300)
	district = models.CharField(max_length=300)
	street = models.CharField(max_length=300)
	estate = models.CharField(max_length=300)
	house_type = models.CharField(max_length=300)
	acreage = models.IntegerField()
	price = models.IntegerField()
	source = models.CharField(max_length=300)
	include_date = models.DateField(auto_now=True)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ('-include_date',)
