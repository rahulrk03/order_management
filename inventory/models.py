from django.db import models


class Product(models.Model):
	product_id = models.CharField(max_length=50, primary_key=True)
	category = models.CharField(max_length=128, null=False, blank=False)
	quantity = models.PositiveIntegerField()
	price = models.DecimalField(decimal_places=2, max_digits=10)
	updated_time = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)
