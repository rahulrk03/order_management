from django.db import models
from inventory.models import Product


class Order(models.Model):
	order_number = models.CharField(primary_key=True, max_length=500)
	customer_name = models.CharField(max_length=256)
	customer_address = models.CharField(max_length=512)
	customer_distance = models.DecimalField(decimal_places=2, max_digits=2)
	order_status = models.CharField(max_length=128)
	total_price = models.DecimalField(decimal_places=2, max_digits=12)
	et_delivery = models.TimeField(auto_now=False, blank=True, null=True)
	created_time = models.DateTimeField(auto_now=False, blank=True, null=True)
	updated_time = models.DateTimeField(auto_now=True, blank=True, null=True)
	team_name = models.CharField(max_length=128, blank=True, null=True)


class OrderDetail(models.Model):
	order_num = models.ForeignKey(Order, on_delete=models.CASCADE)
	product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
	

class DeliveryTeam(models.Model):
	team_name = models.CharField(max_length=500, unique=True)
	is_available = models.BooleanField(default=True)
	available_time = models.DateTimeField(auto_now=False, null=True, blank=True)


class DeliveryAssignment(models.Model):
	team = models.ForeignKey(DeliveryTeam, on_delete=models.CASCADE)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	is_delivered = models.BooleanField(default=False)
	created_time = models.DateTimeField(auto_now=False, blank=True, null=True)
	delivered_time = models.TimeField(auto_now=False, null=True, blank=True)
	updated_time = models.DateTimeField(auto_now=True)
	

