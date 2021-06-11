from django.db import models
from orders.models import DeliveryTeam


# Create your models here.
class Notifications(models.Model):
	message = models.TextField()
	created_time = models.DateTimeField(auto_now=True)
