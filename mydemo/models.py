from django.db import models

# Create your models here.

class Account(models.Model):
	firstname = models.CharField(max_length=255, blank=True, null=True)
	lastname = models.CharField(max_length=255, blank=True, null=True)
	username = models.CharField(max_length=255, blank=True, null=True)
	email = models.CharField(max_length=255, blank=True, null=True)
	phone = models.CharField(max_length=255, blank=True, null=True)
	address = models.CharField(max_length=255, blank=True, null=True)
	password = models.CharField(max_length=255, blank=True, null=True, default="")

   