from django.db import models


# Create your models here.

class ProductCategory(models.Model):
	name = models.CharField(max_length=64)
	description = models.TextField(blank=True, null=True)
