from django.db import models
from django.contrib import admin
# Create your models here.
class estateTrade(models.Model):
	district = models.CharField(max_length=300)
	acreage_amount = models.IntegerField()
	apartment_amount = models.IntegerField()
	trade_date = models.DateField()

	def __unicode__(self):
		return self.district

	class Meta:
		ordering = ('-trade_date',)

admin.site.register(estateTrade)